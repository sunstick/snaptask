#!/usr/bin/env python3
"""
Screenshot Analyzer - Captures screen and sends to OpenAI for analysis
"""

import subprocess
import base64
import os
from datetime import datetime
from openai import OpenAI

def capture_screenshot(output_path):
    """Capture screenshot using macOS screencapture command"""
    try:
        # Use screencapture to take a screenshot
        # -x: no sound, -t png: format, -C: capture cursor
        subprocess.run(['screencapture', '-x', '-t', 'png', output_path], check=True)
        print(f"Screenshot saved to: {output_path}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error capturing screenshot: {e}")
        return False

def encode_image(image_path):
    """Encode image to base64"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def analyze_screenshot(image_path, api_key=None):
    """Send screenshot to OpenAI for analysis"""
    if api_key is None:
        api_key = os.getenv('OPENAI_API_KEY')

    if not api_key:
        raise ValueError("OpenAI API key not found. Set OPENAI_API_KEY environment variable.")

    client = OpenAI(api_key=api_key)

    # Encode the image
    base64_image = encode_image(image_path)

    # Send to OpenAI
    response = client.chat.completions.create(
        model="gpt-4o",  # Using GPT-4 with vision
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": """Analyze this screenshot and provide:
1. What is the user currently focused on or working on?
2. What application/context is visible?
3. What are potential action items or next steps based on what you see?
4. Any patterns or insights about the work being done?

Be concise but insightful."""
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        max_tokens=500
    )

    return response.choices[0].message.content

def main():
    """Main execution flow"""
    # Create ~/.snap directory if it doesn't exist
    screenshots_dir = os.path.expanduser('~/.snap')
    os.makedirs(screenshots_dir, exist_ok=True)

    # Generate timestamp filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    screenshot_path = os.path.join(screenshots_dir, f'screenshot_{timestamp}.png')

    # Capture screenshot
    print("🎨 Capturing screenshot...")
    if not capture_screenshot(screenshot_path):
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
        analysis_path = screenshot_path.replace('.png', '_analysis.txt')
        with open(analysis_path, 'w') as f:
            f.write(analysis)
        print(f"\n💾 Saved analysis to: {analysis_path}")

    except Exception as e:
        print(f"❌ Error analyzing screenshot: {e}")

if __name__ == "__main__":
    main()
