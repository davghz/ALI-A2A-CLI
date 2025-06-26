#!/bin/bash
# Quick Start Script for A2A CLI
# This script helps you get started with the A2A CLI quickly

set -e  # Exit on any error

echo "🚀 A2A CLI Quick Start"
echo "======================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Check if we're in the right directory
if [ ! -f "a2a_cli.py" ]; then
    echo "❌ a2a_cli.py not found. Make sure you're in the a2a-cli directory."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Test installation
echo "🧪 Testing installation..."
python a2a_cli.py --help > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ Installation successful!"
else
    echo "❌ Installation test failed"
    exit 1
fi

# Run basic tests
echo "🔍 Running basic tests..."
python test_cli.py

echo ""
echo "🎉 A2A CLI is ready to use!"
echo ""
echo "Quick commands to try:"
echo "  python a2a_cli.py --help              # Show help"
echo "  python a2a_cli.py agents list         # List agents (requires A2A system)"
echo "  python a2a_cli.py interactive         # Interactive mode"
echo "  python demo_cli.py                    # Run demonstration"
echo ""
echo "📖 For more information, see README.md"
echo ""
echo "Remember to activate the virtual environment in future sessions:"
echo "  source venv/bin/activate" 