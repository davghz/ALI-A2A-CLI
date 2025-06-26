# A2A CLI Makefile
# Common development and deployment tasks

.PHONY: help install test clean demo lint format check setup

# Default target
help:
	@echo "A2A CLI - Available Commands:"
	@echo "=============================="
	@echo "setup     - Initial project setup (venv + dependencies)"
	@echo "install   - Install dependencies"
	@echo "test      - Run tests"
	@echo "demo      - Run demonstration"
	@echo "clean     - Clean up generated files"
	@echo "lint      - Run code linting"
	@echo "format    - Format code"
	@echo "check     - Run all checks (test + lint)"
	@echo "package   - Build package for distribution"
	@echo "help      - Show this help message"

# Setup virtual environment and install dependencies
setup:
	@echo "Setting up A2A CLI development environment..."
	python3 -m venv venv
	@echo "Activate virtual environment with: source venv/bin/activate"
	@echo "Then run: make install"

# Install dependencies
install:
	@echo "Installing dependencies..."
	pip install -r requirements.txt
	@echo "Installation complete!"

# Install in development mode
install-dev:
	@echo "Installing in development mode..."
	pip install -e .
	@echo "Development installation complete!"

# Run tests
test:
	@echo "Running tests..."
	python test_cli.py
	@echo "Tests complete!"

# Run demonstration
demo:
	@echo "Running A2A CLI demonstration..."
	python demo_cli.py

# Quick functionality test
quick-test:
	@echo "Running quick functionality test..."
	python a2a_cli.py --help
	@echo "Quick test complete!"

# Clean up generated files
clean:
	@echo "Cleaning up generated files..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/
	rm -rf dist/
	rm -rf logs/*.log 2>/dev/null || true
	@echo "Cleanup complete!"

# Code linting (if flake8 is available)
lint:
	@echo "Running code linting..."
	@if command -v flake8 >/dev/null 2>&1; then \
		flake8 a2a_cli.py --max-line-length=100; \
	else \
		echo "flake8 not installed. Install with: pip install flake8"; \
	fi

# Code formatting (if black is available)
format:
	@echo "Formatting code..."
	@if command -v black >/dev/null 2>&1; then \
		black a2a_cli.py demo_cli.py test_cli.py --line-length=100; \
	else \
		echo "black not installed. Install with: pip install black"; \
	fi

# Run all checks
check: test lint
	@echo "All checks completed!"

# Build package for distribution
package:
	@echo "Building package..."
	python setup.py sdist bdist_wheel
	@echo "Package built in dist/ directory"

# Show project status
status:
	@echo "A2A CLI Project Status:"
	@echo "======================="
	@echo "Python version: $(shell python --version)"
	@echo "Virtual env: $(VIRTUAL_ENV)"
	@echo "Dependencies:"
	@pip list | grep -E "(click|requests|colorama)" || echo "Dependencies not installed"
	@echo ""
	@echo "Project files:"
	@ls -la *.py *.md *.txt 2>/dev/null || true

# Development server (if applicable)
serve:
	@echo "A2A CLI is a command-line tool, not a server."
	@echo "Try: make demo"

# Install development dependencies
install-dev-deps:
	@echo "Installing development dependencies..."
	pip install flake8 black pytest
	@echo "Development dependencies installed!"

# Run all development tasks
dev-setup: setup install install-dev-deps
	@echo "Development environment setup complete!"
	@echo "Activate with: source venv/bin/activate"

# Verify installation
verify:
	@echo "Verifying A2A CLI installation..."
	python -c "import a2a_cli; print('✅ CLI module imports successfully')"
	python a2a_cli.py --version
	@echo "✅ Installation verified!" 