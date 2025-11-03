#!/usr/bin/env python3
"""
Screenshot Analyzer (OCR Version) - Uses Apple Vision for OCR + GPT-4o-mini for analysis
Much cheaper than full vision API (~15x cost reduction)
"""

import subprocess
import os
from datetime import datetime
from openai import OpenAI
import Quartz
import Vision
from Foundation import NSURL, NSData
import json

def capture_screenshot(output_path):
    """Capture screenshot using macOS screencapture command"""
    try:
        subprocess.run(['screencapture', '-x', '-t', 'png', output_path], check=True)
        print(f"Screenshot saved to: {output_path}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error capturing screenshot: {e}")
        return False

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

def load_prompt(prompt_name, default_prompt):
    """Load prompt from config file or use default"""
    prompts_dir = os.path.expanduser('~/.snap/prompts')
    prompt_file = os.path.join(prompts_dir, prompt_name)

    if os.path.exists(prompt_file):
        with open(prompt_file, 'r') as f:
            return f.read().strip()
    return default_prompt

def analyze_text_with_llm(ocr_result, api_key=None):
    """Send extracted text to GPT-4o-mini for analysis"""
    if api_key is None:
        api_key = os.getenv('OPENAI_API_KEY')

    if not api_key:
        raise ValueError("OpenAI API key not found. Set OPENAI_API_KEY environment variable.")

    client = OpenAI(api_key=api_key)

    if not ocr_result or not ocr_result.get('full_text'):
        return "No text found in screenshot."

    text = ocr_result['full_text']

    # Default prompt
    default_prompt = """Below is text extracted from a user's screenshot. Analyze it and provide:

1. **Current Focus**: What is the user currently working on or focused on?
2. **Context/Application**: Based on the text, what application or context might this be?
3. **Action Items**: What are potential next steps or tasks to complete?
4. **Insights**: Any patterns, blockers, or noteworthy observations?

Be concise but insightful. If the text is insufficient or unclear, say so.

---
EXTRACTED TEXT:
{text}
---"""

    # Load custom prompt or use default
    prompt_template = load_prompt('ocr_prompt.txt', default_prompt)
    user_prompt = prompt_template.replace('{text}', text)

    # Send to OpenAI GPT-4o-mini (much cheaper than GPT-4o)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are an AI assistant that analyzes screen content to help users understand what they're working on and identify action items."
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        max_tokens=400,
        temperature=0.7
    )

    return response.choices[0].message.content

def create_default_prompts():
    """Create default prompt files if they don't exist"""
    prompts_dir = os.path.expanduser('~/.snap/prompts')
    os.makedirs(prompts_dir, exist_ok=True)

    ocr_prompt_file = os.path.join(prompts_dir, 'ocr_prompt.txt')
    if not os.path.exists(ocr_prompt_file):
        default_ocr_prompt = """Below is text extracted from a user's screenshot. Analyze it and provide:

1. **Current Focus**: What is the user currently working on or focused on?
2. **Context/Application**: Based on the text, what application or context might this be?
3. **Action Items**: What are potential next steps or tasks to complete?
4. **Insights**: Any patterns, blockers, or noteworthy observations?

Be concise but insightful. If the text is insufficient or unclear, say so.

---
EXTRACTED TEXT:
{text}
---"""
        with open(ocr_prompt_file, 'w') as f:
            f.write(default_ocr_prompt)

def main():
    """Main execution flow"""
    # Create ~/.snap directory if it doesn't exist
    screenshots_dir = os.path.expanduser('~/.snap')
    os.makedirs(screenshots_dir, exist_ok=True)

    # Create default prompt files if they don't exist
    create_default_prompts()

    # Generate timestamp filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    screenshot_path = os.path.join(screenshots_dir, f'screenshot_{timestamp}.png')

    # Capture screenshot
    print("📸 Capturing screenshot...")
    if not capture_screenshot(screenshot_path):
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
        analysis_path = screenshot_path.replace('.png', '_analysis.txt')
        with open(analysis_path, 'w') as f:
            f.write(analysis)
        print(f"\n💾 Saved analysis to: {analysis_path}")

    except Exception as e:
        print(f"❌ Error analyzing text: {e}")

if __name__ == "__main__":
    main()
