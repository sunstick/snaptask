#!/bin/bash

# SnapTask Uninstaller

set -e

BIN_DIR="/usr/local/bin"
SNAPTASK_BIN="$BIN_DIR/snaptask"

echo "=========================================="
echo "  SnapTask Uninstaller"
echo "=========================================="
echo ""

# Remove symlink
if [ -L "$SNAPTASK_BIN" ]; then
    echo "🗑️  Removing 'snaptask' command..."
    sudo rm "$SNAPTASK_BIN"
    echo "✓ Command removed"
else
    echo "ℹ️  'snaptask' command not found (may already be removed)"
fi
echo ""

echo "Note: This script does not:"
echo "  - Remove Python dependencies (they may be used by other tools)"
echo "  - Remove your data in ~/.snap/ (screenshots and analyses)"
echo "  - Remove the SnapTask repository directory"
echo "  - Remove keyboard shortcuts (remove manually from System Settings)"
echo ""
echo "To fully clean up:"
echo "  - Remove your data: rm -rf ~/.snap/"
echo "  - Remove SnapTask code: delete the repository directory manually"
echo "  - Remove keyboard shortcuts from System Settings → Keyboard"
echo ""
echo "✅ SnapTask uninstalled"
echo ""
