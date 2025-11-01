# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

SnapTask is a macOS productivity tool that captures screenshots and analyzes them using AI to identify what the user is working on and extract action items. It runs via a keyboard shortcut and provides fast, cost-efficient analysis using either local OCR or OpenAI Vision API.

## Architecture

The project consists of three main Python scripts with a CLI wrapper:

### Core Components

1. **snaptask_cli.py** - CLI entry point that routes to the appropriate backend
   - Provides `--vision` flag to switch between modes
   - Checks for OPENAI_API_KEY environment variable
   - Installed globally as `snaptask` command via symlink

2. **snaptask.py** - OCR mode (default, 15x cheaper)
   - Uses Apple Vision framework for local text extraction
   - Sends only extracted text to GPT-4o-mini
   - Cost: ~$0.001 per capture
   - Flow: screencapture → Vision OCR (local) → GPT-4o-mini analysis

3. **snaptask_vision.py** - Vision mode (better for visual content)
   - Sends full screenshot to GPT-4o
   - Cost: ~$0.015 per capture
   - Flow: screencapture → base64 encode → GPT-4o with vision

### Data Storage

All captures saved to `~/.snap/`:
- `screenshot_YYYYMMDD_HHMMSS.png` - Original screenshot
- `screenshot_YYYYMMDD_HHMMSS_ocr.json` - Extracted text (OCR mode only)
- `screenshot_YYYYMMDD_HHMMSS_analysis.txt` - AI analysis

### Installation System

- **install.sh** - Main installer that:
  - Installs Python dependencies from requirements.txt
  - Creates symlink `/usr/local/bin/snaptask → snaptask_cli.py`
  - Creates `~/.snap/` directory
  - Validates Python 3 and pip3 availability

- **uninstall.sh** - Removes `/usr/local/bin/snaptask` symlink only (preserves data)

## Key Dependencies

```
openai>=1.0.0                    # OpenAI API client
pyobjc-framework-Quartz          # macOS screencapture
pyobjc-framework-Vision          # Apple Vision OCR
```

## Development Commands

### Installation & Setup
```bash
# First-time setup (from the repository directory)
./install.sh                     # Install SnapTask and dependencies
./uninstall.sh                   # Remove snaptask command

# Manual installation check
python3 -c "import Vision; import Quartz; print('Dependencies OK')"
```

**Note**: The repository can be located anywhere on the filesystem. The install.sh script auto-detects its location and creates a symlink to `/usr/local/bin/snaptask`.

### Running SnapTask
```bash
snaptask                         # Run with OCR (default)
snaptask --vision                # Run with Vision API
snaptask -v                      # Same as --vision
snaptask --help                  # Show help

# Direct script execution (for testing)
python3 snaptask.py              # Test OCR version
python3 snaptask_vision.py       # Test Vision version
```

### Testing & Debugging
```bash
# Check if command is installed
which snaptask
command -v snaptask

# Test dependencies
python3 -c "import Vision; print('Vision OK')"
python3 -c "import Quartz; print('Quartz OK')"
python3 -c "from openai import OpenAI; print('OpenAI OK')"

# View logs (if using keyboard shortcut)
cat /tmp/screenshot_analyzer.log

# Inspect output files
ls -lh ~/.snap/
cat ~/.snap/screenshot_*_analysis.txt
cat ~/.snap/screenshot_*_ocr.json
```

## Code Modification Guidelines

### Changing the Analysis Prompt

The analysis prompt is in both `snaptask.py` (line ~103) and `snaptask_vision.py` (line ~51). They ask the LLM to provide:
1. Current Focus
2. Context/Application
3. Action Items
4. Insights

Modify these sections to customize the analysis output.

### Switching LLM Providers

**To use Claude (Anthropic)**:
```python
from anthropic import Anthropic
client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
# Replace OpenAI client.chat.completions.create() calls
```

**To use local LLM (Ollama)**:
- Install Ollama
- Replace OpenAI API calls with local inference
- Achieves zero API costs

### Adjusting OCR Confidence

In `snaptask.py:58`, text is filtered by confidence > 0.3. Lower this threshold to capture more text (with potentially lower accuracy), or raise it for higher accuracy (but may miss some text).

### Modifying Screenshot Behavior

Screenshots are captured via `screencapture` command in both files:
- `-x` flag: no sound
- `-t png`: PNG format
- Add `-C` to capture cursor
- Add `-i` for interactive selection

## Environment Configuration

Required:
```bash
export OPENAI_API_KEY="sk-..."
```

The API key is checked by:
1. `install.sh` during installation
2. `snaptask_cli.py` when running
3. Both core scripts when making API calls

## Common Issues

1. **"No module named 'Vision'"** - Run: `pip3 install pyobjc-framework-Vision`
2. **"OpenAI API key not found"** - Set OPENAI_API_KEY in ~/.zshrc
3. **No text extracted** - Check `~/.snap/*_ocr.json` for raw OCR output
4. **Vision mode for visual content** - Use `snaptask --vision` for screenshots with charts, designs, or complex layouts

## Keyboard Shortcut Setup

Users can set up via:
1. macOS Shortcuts app (recommended) - run `snaptask` command
2. Automator workflow - use `setup_shortcut.sh` (legacy)
3. Third-party tools (BetterTouchTool, Karabiner)

See `KEYBOARD_SHORTCUT_SETUP.md` for detailed instructions.
