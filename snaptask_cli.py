#!/usr/bin/env python3
"""
SnapTask CLI - Command-line interface for SnapTask
"""

import argparse
import sys
import os

def run_snaptask(use_vision=False):
    """Run SnapTask with specified mode"""
    if use_vision:
        print("🎨 Running SnapTask (Vision mode)...")
        # Import and run vision mode
        import snaptask_vision
        snaptask_vision.main()
    else:
        print("📝 Running SnapTask (OCR mode)...")
        # Import and run OCR mode
        import snaptask
        snaptask.main()

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
