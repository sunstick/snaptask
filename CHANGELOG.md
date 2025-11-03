# Changelog

## v2.0.0 - Modern Python Packaging (2024-11-03)

### Breaking Changes
- **Migrated to `uv`** for dependency management
- Replaced `requirements.txt` with `pyproject.toml`
- Changed installation: now use `uv sync` instead of `pip install`

### New Features
- ✅ **Single binary distribution** via PyInstaller (17MB)
- ✅ **Modern Python packaging** with `pyproject.toml`
- ✅ **Fast dependency management** with `uv`
- ✅ **Automated build script** (`./build_binary.sh`)
- ✅ No Python installation required for users (binary mode)

### Improvements
- 📦 Simplified dependency management
- 🚀 Faster install times with `uv`
- 📝 Cleaned up documentation
- 🔧 Direct function imports (no subprocess calls)

### Removed
- ❌ `requirements.txt` - replaced by pyproject.toml
- ❌ `requirements-dev.txt` - merged into pyproject.toml
- ❌ `README_SCREENSHOT_ANALYZER.md` - merged into README.md
- ❌ `SNAPTASK_FILES.md` - redundant
- ❌ `snaptask-agent-plan.md` - planning doc
- ❌ `install.sh` - broken, superseded by uv workflow + binary
- ❌ `setup_shortcut.sh` - broken, superseded by Shortcuts app

### Migration Guide

**Before (old way):**
```bash
pip3 install -r requirements.txt
./install.sh
snaptask
```

**After (new way - Binary Distribution):**
```bash
# Build once
./build_binary.sh

# Distribute
dist/snaptask

# Or install system-wide
sudo cp dist/snaptask /usr/local/bin/snaptask
```

**For Developers (source):**
```bash
brew install uv
uv sync
uv run snaptask
```

### Files Structure

```
snaptask/
├── README.md                 # Main documentation
├── CLAUDE.md                 # Developer guide
├── KEYBOARD_SHORTCUT_SETUP.md # Setup instructions
├── pyproject.toml            # Project config
├── uv.lock                   # Dependency lock
├── snaptask_cli.py           # CLI entry
├── snaptask.py               # OCR mode
├── snaptask_vision.py        # Vision mode
├── build_binary.sh           # Binary builder
└── snaptask.spec             # PyInstaller config
```
