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
# Download the binary (from releases or build it yourself)
./snaptask --help

# Set up your API key
export OPENAI_API_KEY="sk-your-key"

# Run it
./snaptask
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

### Set Up Keyboard Shortcut

1. Open **Shortcuts** app
2. Click **+** to create new shortcut
3. Add action: **Run Shell Script**
4. Enter: `snaptask` (or `/full/path/to/snaptask` for binary)
5. Click **(i)** → Check **"Use as Quick Action"**
6. Add keyboard shortcut (e.g., **⌘⇧A** or **⌃⌥S**)
7. Name it **"SnapTask"**

See [KEYBOARD_SHORTCUT_SETUP.md](KEYBOARD_SHORTCUT_SETUP.md) for alternative methods.

## How It Works

```
Press hotkey
    ↓
Capture screenshot (macOS screencapture)
    ↓
Extract text locally (Apple Vision OCR)
    ↓
Analyze with GPT-4o-mini
    ↓
Save to ~/.snap/
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
├── prompts/
│   ├── ocr_prompt.txt                      # OCR mode prompt (editable)
│   └── vision_prompt.txt                   # Vision mode prompt (editable)
├── screenshot_20241103_143022.png          # Original capture
├── screenshot_20241103_143022_ocr.json     # Extracted text (OCR mode)
└── screenshot_20241103_143022_analysis.txt # AI analysis
```

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

```bash
export OPENAI_API_KEY="sk-your-key"
# Add to ~/.zshrc to persist
```

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

- [ ] Change detection (skip unchanged screens)
- [ ] Auto-scheduling (capture every N seconds)
- [ ] Todo.md integration (auto-add action items)
- [ ] Local LLM support (Ollama) - zero cost
- [ ] Activity timeline visualization
- [ ] Focus time tracking
- [ ] Daily/weekly summaries

## Credits

Built with:
- [Apple Vision Framework](https://developer.apple.com/documentation/vision)
- [OpenAI GPT-4o-mini](https://openai.com/index/gpt-4o-mini-advancing-cost-efficient-intelligence/)
- [uv](https://docs.astral.sh/uv/) - Modern Python package manager
- [PyInstaller](https://pyinstaller.org/) - Binary packaging

## License

MIT

---

**Made to help you stay focused and get things done.** 🚀
