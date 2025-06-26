# Contributing to A2A CLI

Thank you for your interest in contributing to the A2A CLI project! This document provides guidelines for contributing to the project.

## Code of Conduct

Please be respectful and considerate in all interactions. We want to maintain a welcoming environment for everyone.

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in [Issues](https://github.com/yourusername/a2a-cli/issues)
2. If not, create a new issue with:
   - Clear description of the bug
   - Steps to reproduce
   - Expected vs actual behavior
   - Your environment (OS, Python version, etc.)
   - Relevant logs or error messages

### Suggesting Features

1. Check if the feature has already been suggested
2. Create a new issue with:
   - Clear description of the feature
   - Use case and benefits
   - Possible implementation approach

### Code Contributions

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/your-feature-name`
3. **Make your changes**
4. **Test your changes**
5. **Commit with clear messages**
6. **Push to your fork**
7. **Create a Pull Request**

## Development Setup

1. **Clone your fork:**
   ```bash
   git clone https://github.com/yourusername/a2a-cli.git
   cd a2a-cli
   ```

2. **Create virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install in development mode:**
   ```bash
   pip install -e .
   pip install -r requirements.txt
   ```

4. **Test the setup:**
   ```bash
   python a2a_cli.py --help
   ```

## Code Style

- Follow PEP 8 Python style guidelines
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and small
- Use type hints where appropriate

### Example Code Style

```python
def submit_task(self, endpoint: str, prompt: str, data: Optional[Dict] = None) -> Dict[str, Any]:
    """Submit a task to an agent.
    
    Args:
        endpoint: The agent endpoint URL
        prompt: The task prompt
        data: Optional additional data
        
    Returns:
        Task submission response
        
    Raises:
        ClickException: If task submission fails
    """
    try:
        payload = {"prompt": prompt}
        if data:
            payload["data"] = data
        
        response = self.session.post(f"{endpoint}/task", json=payload)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        self.logger.error(f"Failed to submit task: {e}")
        raise click.ClickException(f"Failed to submit task: {e}")
```

## Testing

Before submitting changes:

1. **Test basic functionality:**
   ```bash
   python a2a_cli.py --help
   python a2a_cli.py agents list
   ```

2. **Run the demo:**
   ```bash
   python demo_cli.py
   ```

3. **Test edge cases:**
   - Network failures
   - Invalid inputs
   - Missing agents

## Pull Request Guidelines

### PR Title Format
- Use clear, descriptive titles
- Start with a verb: "Add", "Fix", "Update", "Remove"
- Examples:
  - "Add support for custom timeout configuration"
  - "Fix agent health status display issue"
  - "Update documentation for MCP tools"

### PR Description
Include:
- What changes were made
- Why the changes were needed
- How to test the changes
- Any breaking changes
- Screenshots (if UI changes)

### Example PR Template

```markdown
## Description
Brief description of what this PR does.

## Changes
- List of specific changes made
- Another change

## Testing
- [ ] Tested basic CLI functionality
- [ ] Tested new features
- [ ] Updated documentation

## Breaking Changes
None / List any breaking changes

## Screenshots
If applicable, add screenshots here.
```

## Documentation

When adding features:
- Update README.md if needed
- Add docstrings to new functions
- Update help text for new commands
- Consider adding examples

## Project Structure

```
a2a-cli/
├── a2a_cli.py           # Main CLI application
├── requirements.txt     # Dependencies
├── setup.py            # Package setup
├── README.md           # Main documentation
├── INSTALL.md          # Installation guide
├── CONTRIBUTING.md     # This file
├── LICENSE             # MIT license
├── .gitignore          # Git ignore patterns
├── demo_cli.py         # Demo script
└── logs/               # Log files (auto-created)
```

## Areas for Contribution

We welcome contributions in these areas:

### High Priority
- **Error handling improvements**
- **Performance optimizations**
- **Additional output formats** (CSV, YAML)
- **Configuration management enhancements**

### Medium Priority
- **Additional MCP tool integrations**
- **Batch task processing**
- **Agent monitoring dashboards**
- **Plugin architecture**

### Low Priority
- **Shell completions** (bash, zsh, fish)
- **Alternative authentication methods**
- **Export/import configurations**
- **Integration with CI/CD systems**

## Getting Help

- **Questions**: Create a GitHub Discussion
- **Bugs**: Create a GitHub Issue
- **Ideas**: Create a Feature Request Issue
- **Chat**: Join our community channels (if available)

## Recognition

Contributors will be:
- Listed in the project README
- Acknowledged in release notes
- Given appropriate credit for their contributions

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to A2A CLI! 🚀 