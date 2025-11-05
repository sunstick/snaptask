# SnapTask

> Capture your screen, understand your focus, extract action items.

SnapTask is a macOS productivity tool that analyzes your screen to help you understand what you're working on and identify next steps. Press a keyboard shortcut, and it captures your screen, extracts context, and gives you AI-powered insights about your current work.

## Features

- 📸 **One-button capture** - Keyboard shortcut integration
- 🧠 **Smart OCR** - Local Apple Vision for fast, accurate text extraction
- 💰 **Cost-efficient** - 15x cheaper than Vision API (~$0.001/capture)
- 🔒 **Privacy-first** - OCR runs locally, only text sent to LLM
- ⚡ **Fast** - Results in 1-2 seconds
- 📦 **Single binary** - No Python installation required for users
- 📊 **Persistent history** - All captures and analyses saved to `~/.snap/`

## Quick Start

### Option 1: Download Binary (Easiest)

```bash
# Download or build the binary
./snaptask

# First run prompts for API key:
# 🔧 SnapTask First-Time Setup
# Enter your OpenAI API key: [paste key]
# ✅ Configuration saved to ~/.snap/.env

# Interactive screenshot selection appears
# Analysis shown in notification + saved to ~/.snap/
```

### Option 2: Run from Source

Requires [uv](https://docs.astral.sh/uv/) (fast Python package manager):

```bash
# Install uv if needed
brew install uv
# or: curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone and setup
git clone <repo-url> snaptask
cd snaptask
uv sync

# Run
uv run snaptask
```

### Set Up Keyboard Shortcut (Recommended)

**Using Shortcuts App (Built-in, Free):**

1. Open **Shortcuts** app
2. Click **+** to create new shortcut
3. Add action: **Run Shell Script**
4. Enter: `/full/path/to/dist/snaptask` (e.g., `/Users/you/snaptask/dist/snaptask`)
5. Right-click shortcut → **Add Keyboard Shortcut** → Press your key combo (e.g., **⌘⇧S**)
6. Name it **"SnapTask"**

**First run from Shortcuts:**
- You'll get a notification: "Setup Required - Created ~/.snap/.env..."
- Edit `~/.snap/.env` and add your OpenAI API key
- Press hotkey again → it works!

**Alternative methods:** See [KEYBOARD_SHORTCUT_SETUP.md](KEYBOARD_SHORTCUT_SETUP.md) for Automator, Hammerspoon, or paid tools (BetterTouchTool, Keyboard Maestro).

## How It Works

```
Press hotkey
    ↓
Interactive selection (drag area or spacebar for window)
    ↓
Extract text locally (Apple Vision OCR)
    ↓
Analyze with GPT-4o-mini (agentic with file tools)
    ↓
LLM reads existing todo.md & focused.md
    ↓
LLM updates files intelligently (deduplicates)
    ↓
Notification shows analysis summary
    ↓
All saved to ~/.snap/
```

## Usage

```bash
snaptask              # OCR mode (default, recommended)
snaptask --vision     # Vision mode (better for charts/designs)
snaptask --help       # Show help
```

### Two Modes

| Mode | Use Case | Cost | Speed | Privacy |
|------|----------|------|-------|---------|
| **OCR** (default) | Code, terminal, documents | ~$0.001 | 1-2s | Text only to API |
| **Vision** | Design, charts, screenshots | ~$0.015 | 2-4s | Full image to API |

## Example Output

```
📊 ANALYSIS
============================================================
1. **Current Focus**: Debugging Python script errors in
   terminal. Working on Vision framework import issues.

2. **Context/Application**: Terminal/IDE with Python
   traceback visible.

3. **Action Items**:
   - Install pyobjc-framework-Vision dependency
   - Verify environment activation
   - Rerun script to test fix
   - Add error handling for import failures

4. **Insights**: Active troubleshooting session. The user
   needs dependency installation before proceeding.
============================================================
```

## Output Files

All captures and configuration saved to `~/.snap/`:

```
~/.snap/
├── .env                                    # Your OpenAI API key (auto-created)
├── todo.md                                 # AI-maintained todo list (auto-updated!)
├── focused.md                              # Focus tracking with timestamps
├── prompts/
│   ├── ocr_prompt.txt                      # OCR mode prompt (editable)
│   └── vision_prompt.txt                   # Vision mode prompt (editable)
├── screenshot_20241103_143022.png          # Original capture
├── screenshot_20241103_143022_ocr.json     # Extracted text (OCR mode)
└── screenshot_20241103_143022_analysis.txt # Full AI analysis
```

**Key files:**
- **`.env`** - Created on first run, stores your API key securely
- **`todo.md`** - Automatically updated by AI agent (unique todos only)
- **`focused.md`** - Tracks what you're working on over time

## Development

### Build from Source

```bash
# Install dependencies
uv sync

# Run directly
uv run snaptask

# Run with vision mode
uv run snaptask --vision
```

### Build Binary

Create a single executable for distribution:

```bash
./build_binary.sh
# Binary created at: dist/snaptask (17MB)
```

The binary includes all dependencies (Python, OpenAI, PyObjC) - users only need:
- macOS
- OpenAI API key

### Project Structure

```
snaptask/
├── snaptask_cli.py        # CLI entry point
├── snaptask.py            # OCR mode implementation
├── snaptask_vision.py     # Vision mode implementation
├── common.py              # Shared utilities (tools, notifications, config)
├── pyproject.toml         # Dependencies & project config
├── build_binary.sh        # Binary build script
├── snaptask.spec          # PyInstaller config
└── README.md              # This file
```

## Configuration

### Customize Analysis Prompts

SnapTask automatically creates editable prompt files on first run:

- **`~/.snap/prompts/ocr_prompt.txt`** - OCR mode prompt
- **`~/.snap/prompts/vision_prompt.txt`** - Vision mode prompt

**To customize:**

```bash
# Edit the prompts
nano ~/.snap/prompts/ocr_prompt.txt
nano ~/.snap/prompts/vision_prompt.txt

# Changes take effect immediately - no rebuild needed!
```

**Example custom prompt (focus on code review):**

```
Analyze this code and provide:

1. **Code Quality**: Issues, bugs, or improvements
2. **Best Practices**: Are standards being followed?
3. **Security**: Any potential vulnerabilities?
4. **Action Items**: What should be fixed?

Be technical and specific.

---
EXTRACTED TEXT:
{text}
---
```

**Note:** For OCR mode, include `{text}` placeholder. For Vision mode, just write your prompt.

### Switch to Claude

```python
from anthropic import Anthropic
client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
```

### Use Local LLM (Zero Cost)

Install [Ollama](https://ollama.ai/), then replace OpenAI API calls with local inference.

## Cost Estimation

Based on 100 captures/day:

- **OCR version**: ~$3/month
- **Vision version**: ~$45/month

## Privacy & Security

- ✅ **Local OCR** - Apple Vision runs entirely on your device
- ✅ **Text-only** - Only extracted text sent to API (OCR mode)
- ✅ **No telemetry** - All data stays in `~/.snap/`
- ✅ **Full control** - You own all your data
- ⚠️ **Vision mode** - Sends full screenshots to OpenAI

## Troubleshooting

### "command not found: snaptask"

If using source:
```bash
uv run snaptask  # Always use uv run
```

If using binary, ensure it's in PATH or use full path.

### "OpenAI API key not found"

**For terminal usage:**
- Run `snaptask` once - it will prompt for your key interactively
- Or manually edit `~/.snap/.env` and add: `OPENAI_API_KEY=sk-your-key`

**For Shortcuts/GUI usage:**
- First run creates `~/.snap/.env` with placeholder
- Edit the file: `nano ~/.snap/.env`
- Replace `your-api-key-here` with your actual key

### "No text extracted"

- Verify screenshot contains readable text
- Check `~/.snap/*_ocr.json` for raw OCR output
- Try: `snaptask --vision` for better results on visual content

### Build fails

```bash
# Ensure uv is installed
brew install uv

# Sync dependencies
uv sync --extra build

# Try building again
./build_binary.sh
```

## Roadmap

- [x] Todo.md integration (auto-add action items) ✅
- [x] Focus time tracking ✅
- [x] Native notifications ✅
- [x] Interactive screenshot selection ✅
- [ ] Change detection (skip unchanged screens)
- [ ] Auto-scheduling (capture every N seconds)
- [ ] Local LLM support (Ollama) - zero cost
- [ ] Activity timeline visualization
- [ ] Daily/weekly summaries

## Credits

Built with:
- [Apple Vision Framework](https://developer.apple.com/documentation/vision) - Local OCR
- [OpenAI GPT-4o-mini](https://openai.com/index/gpt-4o-mini-advancing-cost-efficient-intelligence/) - AI analysis with function calling
- [python-dotenv](https://github.com/theskumar/python-dotenv) - Environment configuration
- [uv](https://docs.astral.sh/uv/) - Modern Python package manager
- [PyInstaller](https://pyinstaller.org/) - Binary packaging

## License

MIT

---

**Made to help you stay focused and get things done.** 🚀
