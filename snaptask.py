#!/usr/bin/env python3
"""
Screenshot Analyzer (OCR Version) - Uses Apple Vision for OCR + GPT-4o-mini for analysis
Much cheaper than full vision API (~15x cost reduction)
"""

import os
import json
from openai import OpenAI
import Vision
from Foundation import NSURL, NSData
from common import (
    capture_screenshot,
    load_prompt,
    run_agent_loop,
    create_prompt_file,
    get_system_message,
    save_analysis,
    generate_screenshot_path,
    ensure_env_file_exists,
    load_env_config,
    show_notification,
    DEFAULT_OCR_PROMPT
)

def extract_text_with_vision(image_path):
    """Extract text from image using Apple Vision framework"""
    try:
        # Load image
        image_url = NSURL.fileURLWithPath_(image_path)

        # Create Vision request handler
        with open(image_path, 'rb') as f:
            image_data = NSData.dataWithBytes_length_(f.read(), os.path.getsize(image_path))

        # Create text recognition request
        request = Vision.VNRecognizeTextRequest.alloc().init()
        request.setRecognitionLevel_(Vision.VNRequestTextRecognitionLevelAccurate)
        request.setUsesLanguageCorrection_(True)

        # Create request handler and perform request
        handler = Vision.VNImageRequestHandler.alloc().initWithData_options_(image_data, None)
        success = handler.performRequests_error_([request], None)

        if not success[0]:
            print(f"Vision request failed: {success[1]}")
            return None

        # Extract text from results
        observations = request.results()
        text_blocks = []

        for observation in observations:
            text = observation.text()
            confidence = observation.confidence()

            # Only include text with reasonable confidence
            if confidence > 0.3:
                text_blocks.append({
                    'text': text,
                    'confidence': float(confidence)
                })

        # Sort by position (top to bottom, roughly)
        # Vision gives us bounding boxes but for simplicity, just concatenate
        full_text = '\n'.join([block['text'] for block in text_blocks])

        return {
            'full_text': full_text,
            'blocks': text_blocks,
            'total_blocks': len(text_blocks)
        }

    except Exception as e:
        print(f"Error extracting text with Vision: {e}")
        return None


def analyze_text_with_llm(ocr_result, api_key=None):
    """Send extracted text to GPT-4o-mini for analysis with file management tools"""
    if api_key is None:
        api_key = os.getenv('OPENAI_API_KEY')

    if not api_key:
        raise ValueError("OpenAI API key not found. Set OPENAI_API_KEY environment variable.")

    client = OpenAI(api_key=api_key)

    if not ocr_result or not ocr_result.get('full_text'):
        return "No text found in screenshot."

    text = ocr_result['full_text']
    snap_dir = os.path.expanduser('~/.snap')

    # Load custom prompt or use default
    prompt_template = load_prompt('ocr_prompt.txt', DEFAULT_OCR_PROMPT)
    user_prompt = prompt_template.replace('{text}', text)

    # Initialize conversation
    messages = [
        {
            "role": "system",
            "content": get_system_message()
        },
        {
            "role": "user",
            "content": user_prompt
        }
    ]

    # Run agent loop
    return run_agent_loop(client, "gpt-4o-mini", messages, snap_dir)

def create_default_prompts():
    """Create default prompt files if they don't exist"""
    prompts_dir = os.path.expanduser('~/.snap/prompts')
    ocr_prompt_file = os.path.join(prompts_dir, 'ocr_prompt.txt')
    create_prompt_file(ocr_prompt_file, DEFAULT_OCR_PROMPT)

def main():
    """Main execution flow"""
    # Ensure .env file exists and is configured
    if not ensure_env_file_exists():
        return  # Setup needed, exit gracefully

    # Load environment from ~/.snap/.env
    load_env_config()

    # Create default prompt files if they don't exist
    create_default_prompts()

    # Generate screenshot path
    screenshot_path = generate_screenshot_path()

    # Capture screenshot
    print("📸 Capturing screenshot...")
    print("   → Drag to select area, or press SPACE to select window, ESC to cancel")
    if not capture_screenshot(screenshot_path):
        print("   Screenshot canceled or failed")
        return

    # Extract text using Apple Vision
    print("🔍 Extracting text with Apple Vision OCR...")
    ocr_result = extract_text_with_vision(screenshot_path)

    if ocr_result:
        print(f"   Found {ocr_result['total_blocks']} text blocks")

        # Save OCR result for debugging
        ocr_path = screenshot_path.replace('.png', '_ocr.json')
        with open(ocr_path, 'w') as f:
            json.dump(ocr_result, f, indent=2)
    else:
        print("   No text extracted")
        return

    # Analyze with LLM
    print("\n🤖 Analyzing with GPT-4o-mini...")
    try:
        analysis = analyze_text_with_llm(ocr_result)
        print("\n" + "="*60)
        print("📊 ANALYSIS")
        print("="*60)
        print(analysis)
        print("="*60)

        # Save analysis
        analysis_path = save_analysis(screenshot_path, analysis)
        print(f"\n💾 Saved analysis to: {analysis_path}")

        # Show notification with analysis summary (truncate if too long)
        notification_text = analysis[:200] + "..." if len(analysis) > 200 else analysis
        show_notification("SnapTask Analysis", notification_text)

    except Exception as e:
        print(f"❌ Error analyzing text: {e}")
        show_notification("SnapTask Error", f"Analysis failed: {str(e)[:100]}")

if __name__ == "__main__":
    main()
