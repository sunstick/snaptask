# SnapTask

> Capture your screen, understand your focus, extract action items.

SnapTask is a macOS productivity tool that analyzes your screen to help you understand what you're working on and identify next steps. Press a keyboard shortcut, and it captures your screen, extracts context, and gives you insights about your current work.

## Why SnapTask?

Ever feel like you're context-switching constantly but can't remember what you were supposed to do? SnapTask helps you:

- **Track your focus** - Know what you were actually working on
- **Extract action items** - Automatically identify next steps from your screen
- **Build work patterns** - Understand how you spend your time
- **Reduce cognitive load** - Let AI remember the details

## Features

- 📸 **One-button capture** - Keyboard shortcut to capture and analyze
- 🧠 **Smart OCR** - Uses Apple Vision for fast, accurate text extraction
- 💰 **Cost-efficient** - 15x cheaper than full vision API (~$0.001/capture)
- 🔒 **Privacy-first** - OCR runs locally, only text sent to LLM
- ⚡ **Fast** - Results in 1-2 seconds
- 📊 **Persistent history** - All captures and analyses saved

## Quick Start

### 1. Install

Clone the repository and run the installer:

```bash
git clone <repository-url> snaptask
cd snaptask
./install.sh
```

Or if you already have the repository:

```bash
cd snaptask  # Navigate to wherever you cloned/placed the repository
./install.sh
```

This will:
- Install Python dependencies
- Set up the `snaptask` command globally
- Create necessary directories

### 2. Configure API Key

Add to your `~/.zshrc`:

```bash
export OPENAI_API_KEY="sk-your-api-key-here"
```

Reload shell:
```bash
source ~/.zshrc
```

### 3. Test

```bash
snaptask              # OCR mode (default)
snaptask --vision     # Vision mode
snaptask --help       # Show help
```

### 4. Set up keyboard shortcut

**Easiest method** (macOS Shortcuts app):

1. Open **Shortcuts** app
2. Click **+** to create new shortcut
3. Add action: **Run Shell Script**
4. Paste: `snaptask`
5. Click **(i)** info button → Check **"Use as Quick Action"**
6. Add keyboard shortcut (e.g., **⌘⇧A** or **⌃⌥S**)
7. Name it **"SnapTask"**

See `KEYBOARD_SHORTCUT_SETUP.md` for alternative methods.

## How It Works

```
Press hotkey
    ↓
Capture screenshot (macOS screencapture)
    ↓
Extract text (Apple Vision OCR - local, fast)
    ↓
Analyze context (GPT-4o-mini)
    ↓
Save to ~/.snap/ (screenshots + analysis + action items)
```

## Example Output

```
📊 ANALYSIS
============================================================
1. **Current Focus**: Debugging a Python script related to
   screenshot analysis functionality. Looking at error logs
   and code implementation.

2. **Context/Application**: Terminal/IDE - likely VS Code or
   Terminal with Python traceback visible.

3. **Action Items**:
   - Fix ModuleNotFoundError for Vision framework
   - Install pyobjc-framework-Vision dependency
   - Rerun the script to verify the fix
   - Test OCR extraction on sample screenshot

4. **Insights**: The user is actively troubleshooting import
   errors. Next logical step is dependency installation.
============================================================
```

## Versions

SnapTask comes in two flavors:

| Version | Use Case | Cost/Capture | Speed |
|---------|----------|--------------|-------|
| **OCR** (default) | Code, terminal, documents | ~$0.001 | 1-2s |
| **Vision** | Design, charts, visual work | ~$0.015 | 2-4s |

**Default is OCR** - works great for 90% of knowledge work.

To use Vision version: `snaptask --vision`

## Output Files

All files saved to `~/.snap/`:

```
~/.snap/
├── screenshot_20241101_143022.png          # Original capture
├── screenshot_20241101_143022_ocr.json     # Extracted text (OCR mode)
└── screenshot_20241101_143022_analysis.txt # AI analysis
```

This keeps your data separate from the application code and makes it easy to find all your captures in one place.

## Cost Estimation

Based on 100 captures/day:

- **OCR version**: ~$3/month
- **Vision version**: ~$45/month

## Roadmap

Future enhancements:

- [ ] Automatic scheduling (capture every N seconds)
- [ ] Change detection (skip unchanged screens)
- [ ] Integration with todo.md (auto-add action items)
- [ ] Local LLM support (Ollama) for zero-cost operation
- [ ] Activity timeline visualization
- [ ] Focus time tracking
- [ ] Smart summaries (daily/weekly work summary)

## Configuration

### Change the analysis prompt

Edit the prompt in `snaptask.py` (line ~95) to customize what insights you want.

### Switch to Claude

Replace OpenAI client with Anthropic:

```python
from anthropic import Anthropic
client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
```

### Use local LLM (free!)

Install Ollama, then replace the OpenAI call with local inference. Zero API costs.

## Troubleshooting

**"No module named 'Vision'"**
```bash
pip3 install pyobjc-framework-Vision
```

**"OpenAI API key not found"**
```bash
export OPENAI_API_KEY="your-key"
source ~/.zshrc
```

**Keyboard shortcut not working**
- Check that Shortcuts app has accessibility permissions
- Verify the script path in your shortcut
- Check `/tmp/screenshot_analyzer.log` for errors

**No text extracted**
- Verify screenshot contains readable text
- Check `~/.snap/*_ocr.json` for raw OCR output
- Try the Vision version if OCR isn't working

**Managing your data**
- View all captures: `ls -lh ~/.snap/`
- Clear old captures: `rm ~/.snap/screenshot_2024*`
- Backup your data: `cp -r ~/.snap ~/backup/snap_backup`

## Privacy & Security

- **Local OCR** - Apple Vision runs entirely on your device
- **Text only to API** - Only extracted text sent to OpenAI, not images (Vision mode sends full image)
- **No telemetry** - All data stays on your machine in `~/.snap/`
- **API key** - Stored in your local environment only
- **Full control** - All screenshots and analyses saved locally, you own your data

For maximum privacy, use the local LLM option (coming soon).

## License

MIT

## Credits

Built with:
- [Apple Vision Framework](https://developer.apple.com/documentation/vision)
- [OpenAI GPT-4o-mini](https://openai.com/index/gpt-4o-mini-advancing-cost-efficient-intelligence/)
- macOS screencapture

---

**Made to help you stay focused and get things done.** 🚀
