# SnapTask Project Files

## Core Files

| File | Purpose |
|------|---------|
| `snaptask.py` | Main OCR version (Apple Vision + GPT-4o-mini) - **Recommended** |
| `snaptask_vision.py` | Vision API version (GPT-4o with vision) - For visual content |
| `snaptask_cli.py` | CLI wrapper that provides `snaptask` command |

## Installation & Setup

| File | Purpose |
|------|---------|
| `install.sh` | Installer script - sets up everything |
| `uninstall.sh` | Uninstaller script |
| `requirements.txt` | Python dependencies |

## Documentation

| File | Purpose |
|------|---------|
| `README.md` | Main documentation - **Start here** |
| `CLAUDE.md` | Guidance for Claude Code when working in this repository |
| `KEYBOARD_SHORTCUT_SETUP.md` | Keyboard shortcut setup guide |
| `SNAPTASK_FILES.md` | This file - project overview |

## Legacy Files (can be deleted)

| File | Purpose |
|------|---------|
| `screenshot_analyzer.py` | Old name for `snaptask_vision.py` |
| `screenshot_analyzer_ocr.py` | Old name for `snaptask.py` |
| `setup_shortcut.sh` | Old Automator setup script (superseded by Shortcuts app method) |
| `README_SCREENSHOT_ANALYZER.md` | Old README (superseded by README.md) |

## Generated Files (User Data)

| Location | Purpose |
|----------|---------|
| `~/.snap/` | All captured screenshots and analyses |
| `~/.snap/screenshot_*.png` | Captured screenshots |
| `~/.snap/screenshot_*_ocr.json` | Extracted text (OCR version only) |
| `~/.snap/screenshot_*_analysis.txt` | AI analysis results |

**Note:** User data is stored in `~/.snap/` to keep it separate from the application code.

## Installation Commands

```bash
# Install (from the repository directory)
./install.sh

# Test
snaptask

# Uninstall
./uninstall.sh
```

## Command Usage

```bash
snaptask              # Run with OCR mode (default, cheaper)
snaptask --vision     # Run with Vision mode (better for visual content)
snaptask --help       # Show help
snaptask --version    # Show version
```
