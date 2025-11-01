#!/usr/bin/env python3
"""
SnapTask CLI - Command-line interface for SnapTask
"""

import argparse
import sys
import os
import subprocess

# Get the directory where SnapTask is installed
SNAPTASK_DIR = os.path.dirname(os.path.abspath(__file__))

def run_snaptask(use_vision=False):
    """Run SnapTask with specified mode"""
    if use_vision:
        script = os.path.join(SNAPTASK_DIR, 'snaptask_vision.py')
        print("🎨 Running SnapTask (Vision mode)...")
    else:
        script = os.path.join(SNAPTASK_DIR, 'snaptask.py')
        print("📝 Running SnapTask (OCR mode)...")

    try:
        subprocess.run([sys.executable, script], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running SnapTask: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print(f"❌ SnapTask script not found at: {script}")
        print("   Run the installer first from the SnapTask directory: ./install.sh")
        sys.exit(1)

def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description='SnapTask - Capture your screen, understand your focus, extract action items.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  snaptask              # Capture and analyze (OCR mode)
  snaptask --vision     # Capture and analyze (Vision mode)
  snaptask -v           # Same as --vision

For more info, see: README.md in the SnapTask repository
        """
    )

    parser.add_argument(
        '-v', '--vision',
        action='store_true',
        help='Use OpenAI Vision API instead of OCR (better for visual content, more expensive)'
    )

    parser.add_argument(
        '--version',
        action='version',
        version='SnapTask 1.0.0'
    )

    args = parser.parse_args()

    # Check if OpenAI API key is set
    if not os.getenv('OPENAI_API_KEY'):
        print("⚠️  Warning: OPENAI_API_KEY environment variable not set")
        print("   Add to your ~/.zshrc: export OPENAI_API_KEY='sk-...'")
        print("   Then: source ~/.zshrc")
        print()

    run_snaptask(use_vision=args.vision)

if __name__ == '__main__':
    main()
