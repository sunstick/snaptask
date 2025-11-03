#!/bin/bash

# build_binary.sh
# Builds SnapTask into a single self-contained binary using PyInstaller + uv

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Building SnapTask Binary with PyInstaller${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Check if we're in the right directory
if [ ! -f "snaptask_cli.py" ]; then
    echo -e "${RED}Error: Must run this script from the SnapTask repository directory${NC}"
    exit 1
fi

# Check if uv is installed
echo -e "${BLUE}Checking for uv...${NC}"
if ! command -v uv &> /dev/null; then
    echo -e "${RED}✗ uv not found${NC}"
    echo ""
    echo -e "${YELLOW}Please install uv first:${NC}"
    echo "  curl -LsSf https://astral.sh/uv/install.sh | sh"
    echo "  or"
    echo "  brew install uv"
    echo ""
    exit 1
else
    UV_VERSION=$(uv --version)
    echo -e "${GREEN}✓ uv found ($UV_VERSION)${NC}"
fi
echo ""

# Sync dependencies (creates .venv if needed, installs all deps including PyInstaller)
echo -e "${BLUE}Syncing dependencies with uv...${NC}"
uv sync --extra build
echo -e "${GREEN}✓ Dependencies synced${NC}"
echo ""

# Clean previous builds
if [ -d "build" ] || [ -d "dist" ]; then
    echo -e "${YELLOW}Cleaning previous build artifacts...${NC}"
    rm -rf build dist
    echo -e "${GREEN}✓ Cleaned${NC}"
    echo ""
fi

# Build the binary using uv run
echo -e "${BLUE}Building binary (this may take 1-2 minutes)...${NC}"
uv run pyinstaller snaptask.spec

echo ""

# Check if build succeeded
if [ -f "dist/snaptask" ]; then
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}✓ Binary created successfully!${NC}"
    echo -e "${GREEN}========================================${NC}"
    echo ""
    echo -e "Location: ${BLUE}dist/snaptask${NC}"
    echo -e "Size: ${BLUE}$(du -h dist/snaptask | cut -f1)${NC}"
    echo ""

    # Test the binary
    echo -e "${BLUE}Testing binary...${NC}"
    if dist/snaptask --help > /dev/null 2>&1; then
        echo -e "${GREEN}✓ Binary runs successfully${NC}"
    else
        echo -e "${YELLOW}⚠ Warning: Binary may have issues (but this could be due to missing API key)${NC}"
    fi
    echo ""

    # Offer to install
    echo -e "${YELLOW}Installation Options:${NC}"
    echo "1. Install to /usr/local/bin (system-wide)"
    echo "2. Keep in dist/ directory (manual installation)"
    echo "3. Skip installation"
    echo ""
    read -p "Choose option (1/2/3): " -n 1 -r
    echo ""

    if [[ $REPLY == "1" ]]; then
        echo -e "${BLUE}Installing to /usr/local/bin...${NC}"
        sudo cp dist/snaptask /usr/local/bin/snaptask
        sudo chmod +x /usr/local/bin/snaptask
        echo -e "${GREEN}✓ Installed to /usr/local/bin/snaptask${NC}"
        echo ""
        echo -e "${GREEN}You can now run 'snaptask' from anywhere!${NC}"
    elif [[ $REPLY == "2" ]]; then
        echo ""
        echo -e "${BLUE}To install manually later, run:${NC}"
        echo "  sudo cp dist/snaptask /usr/local/bin/snaptask"
        echo "  sudo chmod +x /usr/local/bin/snaptask"
    else
        echo -e "${BLUE}Skipping installation${NC}"
    fi

    echo ""
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}Build complete!${NC}"
    echo -e "${GREEN}========================================${NC}"
    echo ""
    echo -e "${YELLOW}Note:${NC} You still need to set OPENAI_API_KEY environment variable:"
    echo "  export OPENAI_API_KEY=\"sk-...\""

else
    echo -e "${RED}========================================${NC}"
    echo -e "${RED}✗ Build failed${NC}"
    echo -e "${RED}========================================${NC}"
    echo ""
    echo "Check the output above for errors."
    echo "Common issues:"
    echo "  - Missing dependencies: uv sync --extra build"
    echo "  - PyObjC frameworks not found: Check pyproject.toml dependencies"
    exit 1
fi
