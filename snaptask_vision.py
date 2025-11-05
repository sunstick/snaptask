#!/usr/bin/env python3
"""
Screenshot Analyzer - Captures screen and sends to OpenAI for analysis
"""

import base64
import os
from openai import OpenAI
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
    DEFAULT_VISION_PROMPT
)


def encode_image(image_path):
    """Encode image to base64"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def analyze_screenshot(image_path, api_key=None):
    """Send screenshot to OpenAI for analysis with file management tools"""
    if api_key is None:
        api_key = os.getenv('OPENAI_API_KEY')

    if not api_key:
        raise ValueError("OpenAI API key not found. Set OPENAI_API_KEY environment variable.")

    client = OpenAI(api_key=api_key)
    snap_dir = os.path.expanduser('~/.snap')

    # Encode the image
    base64_image = encode_image(image_path)

    # Load custom prompt or use default
    vision_prompt = load_prompt('vision_prompt.txt', DEFAULT_VISION_PROMPT)

    # Initialize conversation
    messages = [
        {
            "role": "system",
            "content": get_system_message()
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": vision_prompt
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{base64_image}"
                    }
                }
            ]
        }
    ]

    # Run agent loop
    return run_agent_loop(client, "gpt-4o", messages, snap_dir)

def create_default_prompts():
    """Create default prompt files if they don't exist"""
    prompts_dir = os.path.expanduser('~/.snap/prompts')
    vision_prompt_file = os.path.join(prompts_dir, 'vision_prompt.txt')
    create_prompt_file(vision_prompt_file, DEFAULT_VISION_PROMPT)

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
    print("🎨 Capturing screenshot...")
    print("   → Drag to select area, or press SPACE to select window, ESC to cancel")
    if not capture_screenshot(screenshot_path):
        print("   Screenshot canceled or failed")
        return

    # Analyze with OpenAI
    print("\n🤖 Analyzing screenshot with OpenAI Vision...")
    try:
        analysis = analyze_screenshot(screenshot_path)
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
        print(f"❌ Error analyzing screenshot: {e}")
        show_notification("SnapTask Error", f"Analysis failed: {str(e)[:100]}")

if __name__ == "__main__":
    main()
