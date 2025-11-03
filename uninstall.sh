#!/bin/bash

# SnapTask Uninstaller
# Removes the snaptask command from your system

set -e

BIN_DIR="/usr/local/bin"
SNAPTASK_BIN="$BIN_DIR/snaptask"

echo "=========================================="
echo "  SnapTask Uninstaller"
echo "=========================================="
echo ""

# Check what kind of installation exists
if [ -f "$SNAPTASK_BIN" ]; then
    if [ -L "$SNAPTASK_BIN" ]; then
        echo "🗑️  Found symlink installation at $SNAPTASK_BIN"
        echo "    Removing symlink..."
        sudo rm "$SNAPTASK_BIN"
        echo "✓ Symlink removed"
    else
        echo "🗑️  Found binary installation at $SNAPTASK_BIN"
        read -p "Remove binary? (y/n) " -n 1 -r
        echo ""
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            sudo rm "$SNAPTASK_BIN"
            echo "✓ Binary removed"
        else
            echo "Skipped binary removal"
        fi
    fi
else
    echo "ℹ️  'snaptask' command not found in $BIN_DIR"
    echo "   (may already be removed)"
fi
echo ""

echo "=========================================="
echo "What this script does NOT remove:"
echo "=========================================="
echo "  - Your data in ~/.snap/ (screenshots and analyses)"
echo "  - The SnapTask repository/source code"
echo "  - Python dependencies installed via uv"
echo "  - Keyboard shortcuts (remove from System Settings)"
echo ""
echo "To fully clean up:"
echo "  - Remove data:         rm -rf ~/.snap/"
echo "  - Remove source:       delete the repository directory"
echo "  - Remove shortcuts:    System Settings → Keyboard → Shortcuts"
echo "  - Remove .venv:        rm -rf .venv/"
echo ""
echo "✅ Uninstall complete"
echo ""
