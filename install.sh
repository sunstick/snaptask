#!/bin/bash

# SnapTask Installer
# Installs SnapTask and sets up CLI command

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
BIN_DIR="/usr/local/bin"
SNAPTASK_BIN="$BIN_DIR/snaptask"

echo "=========================================="
echo "  SnapTask Installer"
echo "=========================================="
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"
echo ""

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip3 first."
    exit 1
fi

echo "✓ pip3 found"
echo ""

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip3 install -q -r "$SCRIPT_DIR/requirements.txt"

if [ $? -eq 0 ]; then
    echo "✓ Dependencies installed"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi
echo ""

# Create symlink for CLI command
echo "🔗 Setting up 'snaptask' command..."

# Check if /usr/local/bin exists, create if not
if [ ! -d "$BIN_DIR" ]; then
    echo "   Creating $BIN_DIR directory..."
    sudo mkdir -p "$BIN_DIR"
fi

# Remove old symlink if it exists
if [ -L "$SNAPTASK_BIN" ]; then
    echo "   Removing old symlink..."
    sudo rm "$SNAPTASK_BIN"
fi

# Create new symlink
sudo ln -s "$SCRIPT_DIR/snaptask_cli.py" "$SNAPTASK_BIN"

if [ $? -eq 0 ]; then
    echo "✓ Command 'snaptask' installed to $SNAPTASK_BIN"
else
    echo "❌ Failed to create symlink. You may need sudo access."
    exit 1
fi
echo ""

# Check if OPENAI_API_KEY is set
echo "🔑 Checking for OpenAI API key..."
if [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️  OPENAI_API_KEY not found in environment"
    echo ""
    echo "To set it up:"
    echo "1. Add to your ~/.zshrc or ~/.bash_profile:"
    echo "   export OPENAI_API_KEY='sk-your-api-key-here'"
    echo ""
    echo "2. Reload your shell:"
    echo "   source ~/.zshrc"
    echo ""
else
    echo "✓ OPENAI_API_KEY is set"
fi
echo ""

# Create ~/.snap directory for storing screenshots and analyses
SNAP_DIR="$HOME/.snap"
if [ ! -d "$SNAP_DIR" ]; then
    mkdir -p "$SNAP_DIR"
    echo "✓ Created SnapTask data directory: $SNAP_DIR"
    echo ""
fi

# Test installation
echo "🧪 Testing installation..."
if command -v snaptask &> /dev/null; then
    echo "✓ 'snaptask' command is available"
else
    echo "❌ 'snaptask' command not found in PATH"
    echo "   You may need to restart your terminal"
fi
echo ""

echo "=========================================="
echo "  ✅ Installation Complete!"
echo "=========================================="
echo ""
echo "Quick Start:"
echo "  snaptask              # Run SnapTask (OCR mode)"
echo "  snaptask --vision     # Run SnapTask (Vision mode)"
echo "  snaptask --help       # Show help"
echo ""
echo "Next Steps:"
echo "1. Set up your OpenAI API key (if not done yet)"
echo "2. Test: snaptask"
echo "3. Set up keyboard shortcut (see KEYBOARD_SHORTCUT_SETUP.md)"
echo ""
echo "Documentation: $SCRIPT_DIR/README.md"
echo ""
