#!/bin/bash
# DevCLI Quick Install Script
# Usage: curl -sSL https://raw.githubusercontent.com/YOUR_USERNAME/devcli/main/install.sh | bash

set -e

echo "🚀 Installing DevCLI..."
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not found."
    echo "   Install Python 3.8+ from: https://python.org"
    exit 1
fi

# Check pip
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip is required but not found."
    echo "   Install pip: python3 -m ensurepip --upgrade"
    exit 1
fi

# Install DevCLI
echo "📦 Installing DevCLI from PyPI..."
pip3 install devcli

# Check installation
if command -v devcli &> /dev/null; then
    echo ""
    echo "✅ DevCLI installed successfully!"
    echo ""
    echo "🎉 Quick Start:"
    echo "   1. Install Ollama: https://ollama.ai"
    echo "   2. Pull a model: ollama pull llama3.1"
    echo "   3. Try DevCLI: devcli hello"
    echo ""
    echo "📚 Full docs: https://github.com/YOUR_USERNAME/devcli"
else
    echo ""
    echo "⚠️  Installation completed but 'devcli' command not found."
    echo "   Try: python3 -m devcli"
    echo "   Or add ~/.local/bin to your PATH"
fi
