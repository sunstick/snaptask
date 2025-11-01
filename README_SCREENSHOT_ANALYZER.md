# Screenshot Analyzer

Two versions available based on your needs:

## Version Comparison

| Feature | Vision API (`screenshot_analyzer.py`) | OCR + LLM (`screenshot_analyzer_ocr.py`) |
|---------|--------------------------------------|------------------------------------------|
| **Cost per screenshot** | ~$0.015 | ~$0.001 |
| **Speed** | 2-4 seconds | 1-2 seconds |
| **Context** | Full visual (UI, charts, images) | Text only |
| **Privacy** | Sends full screenshot to OpenAI | Extracts text locally, sends text only |
| **Best for** | Design work, data viz, mixed content | Code, terminal, text-heavy work |
| **Dependencies** | `openai` | `openai`, `pyobjc-framework-Vision` |

## Setup

### 1. Install dependencies

```bash
# From the repository directory
pip3 install -r requirements.txt
```

### 2. Set OpenAI API key

Add to your `~/.zshrc` or `~/.bash_profile`:

```bash
export OPENAI_API_KEY="sk-your-api-key-here"
```

Then reload:
```bash
source ~/.zshrc
```

### 3. Test the scripts

**OCR version (recommended for most cases):**
```bash
python3 screenshot_analyzer_ocr.py
```

**Vision version (for visual content):**
```bash
python3 screenshot_analyzer.py
```

### 4. Set up keyboard shortcut

See `KEYBOARD_SHORTCUT_SETUP.md` for instructions.

To use the OCR version with keyboard shortcut, just replace `screenshot_analyzer.py` with `screenshot_analyzer_ocr.py` in the shortcut command.

## Output

Both scripts save:
- Screenshot: `screenshots/screenshot_YYYYMMDD_HHMMSS.png`
- Analysis: `screenshots/screenshot_YYYYMMDD_HHMMSS_analysis.txt`
- OCR data (OCR version only): `screenshots/screenshot_YYYYMMDD_HHMMSS_ocr.json`

## Cost Estimation

If you capture 100 screenshots/day:

- **Vision API**: ~$1.50/day = $45/month
- **OCR + LLM**: ~$0.10/day = $3/month

**15x cheaper with OCR approach!**

## Recommendation

**Use OCR version** (`screenshot_analyzer_ocr.py`) if your work is:
- Writing code
- Terminal/command line work
- Reading/writing documents
- Web browsing with text content

**Use Vision version** (`screenshot_analyzer.py`) if you're:
- Designing in Figma/Sketch
- Working with charts/graphs
- Editing images/videos
- Need full UI context

## Future Enhancements

Possible additions:
- Change detection to avoid redundant captures
- Automatic scheduling (every 30s in background)
- Integration with todo.md for automatic action item extraction
- Local LLM option (Ollama) for complete privacy
