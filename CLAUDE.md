# CLAUDE.md

This file provides guidance to Claude Code when working with code in this repository.

## Project Overview

SnapTask is a macOS productivity tool that captures screenshots and analyzes them using AI to identify what the user is working on and extract action items. It runs via a keyboard shortcut and provides fast, cost-efficient analysis using either local OCR or OpenAI Vision API.

## Architecture

Modern Python project managed with **uv** (fast package manager).

### Core Components

1. **snaptask_cli.py** - CLI entry point
   - Provides `--vision` flag to switch between modes
   - Imports and calls main() from backend modules directly
   - Installed as `snaptask` command via pyproject.toml

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

### Dependency Management

**Everything is managed with uv:**
- `pyproject.toml` - Project configuration and dependencies
- `uv.lock` - Locked dependency versions
- `.venv/` - Virtual environment (created by `uv sync`)

## Development Commands

### Setup & Running

```bash
# First-time setup
uv sync                      # Install all dependencies

# Run the tool
uv run snaptask              # OCR mode
uv run snaptask --vision     # Vision mode
uv run snaptask --help       # Show help

# Direct script execution (for testing)
uv run python snaptask.py    # Test OCR version
uv run python snaptask_vision.py  # Test Vision version
```

### Building Binary

```bash
# Build single-file executable (17MB)
./build_binary.sh            # Creates dist/snaptask

# The binary includes:
# - Python 3.13.2
# - All dependencies (openai, pyobjc, etc.)
# - All three Python modules

# Users only need:
# - macOS
# - OPENAI_API_KEY environment variable
```

### Testing & Debugging

```bash
# Check dependencies
uv pip list

# View output files
ls -lh ~/.snap/
cat ~/.snap/screenshot_*_analysis.txt

# Test binary
dist/snaptask --help
OPENAI_API_KEY=test dist/snaptask  # Will fail at API call, but tests imports
```

## Key Dependencies

Defined in `pyproject.toml`:

```toml
dependencies = [
    "openai>=1.0.0",                 # OpenAI API client
    "pyobjc-framework-Quartz",       # macOS screencapture
    "pyobjc-framework-Vision",       # Apple Vision OCR
]

[project.optional-dependencies]
build = [
    "pyinstaller>=6.0.0",            # Binary packaging
]
```

## Code Modification Guidelines

### Changing the Analysis Prompt

**User-Facing (Recommended):**

Prompts are automatically created in `~/.snap/prompts/` on first run:
- `~/.snap/prompts/ocr_prompt.txt` - OCR mode
- `~/.snap/prompts/vision_prompt.txt` - Vision mode

Users can edit these files directly - no code changes or rebuild needed!

**Developer-Facing:**

Default prompts are defined in:
- `snaptask.py` - `create_default_prompts()` function (line ~141)
- `snaptask_vision.py` - `create_default_prompts()` function (line ~89)

The prompts ask for:
1. Current Focus
2. Context/Application
3. Action Items
4. Insights

**How it works:**
1. On first run, default prompts are written to `~/.snap/prompts/`
2. Subsequent runs load from these files
3. Users can edit the files to customize behavior
4. If files are deleted, defaults are recreated

### Adding Dependencies

```bash
# Add a new dependency
uv add package-name

# Add a dev/build dependency
uv add --optional build package-name

# Update lockfile
uv lock
```

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

The API key is checked by `snaptask_cli.py` and both core scripts.

## Common Issues

1. **"command not found: snaptask"** - Use `uv run snaptask` when running from source
2. **"No module named 'openai'"** - Run: `uv sync` to install dependencies
3. **"OpenAI API key not found"** - Set OPENAI_API_KEY in environment
4. **No text extracted** - Check `~/.snap/*_ocr.json` for raw OCR output
5. **Vision mode for visual content** - Use `snaptask --vision` for screenshots with charts, designs, or complex layouts
6. **Build fails** - Run `uv sync --extra build` to install PyInstaller

## Binary Build Process

1. `./build_binary.sh` checks for uv
2. `uv sync --extra build` installs all dependencies + PyInstaller in `.venv`
3. `uv run pyinstaller snaptask.spec` builds the binary
4. Result: `dist/snaptask` (17MB self-contained executable)

The spec file (`snaptask.spec`) tells PyInstaller to:
- Bundle all 3 Python modules
- Include PyObjC frameworks
- Include OpenAI and dependencies
- Create single-file executable

## Keyboard Shortcut Setup

Users set up via:
1. macOS Shortcuts app (recommended) - run `snaptask` command or binary path
2. BetterTouchTool
3. Alfred workflows

See `KEYBOARD_SHORTCUT_SETUP.md` for detailed instructions.

## Project Files

### Core
- `snaptask_cli.py` - CLI entry point
- `snaptask.py` - OCR implementation
- `snaptask_vision.py` - Vision implementation

### Configuration
- `pyproject.toml` - Project config, dependencies, entry points
- `uv.lock` - Locked dependencies
- `snaptask.spec` - PyInstaller configuration

### Scripts
- `build_binary.sh` - Build single-file executable (17MB)
- `uninstall.sh` - Remove snaptask from /usr/local/bin

### Documentation
- `README.md` - Main user documentation
- `CLAUDE.md` - This file
- `KEYBOARD_SHORTCUT_SETUP.md` - Keyboard shortcut instructions
