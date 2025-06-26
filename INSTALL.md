# Installation Guide

This guide will help you install and set up the A2A CLI for interacting with your multi-agent system.

## Prerequisites

- **Python 3.8+**: Make sure you have Python 3.8 or higher installed
- **pip**: Python package installer (usually comes with Python)
- **A2A Multi-Agent System**: The CLI requires a running A2A multi-agent system

## Quick Installation

### Method 1: Direct Installation (Recommended)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/a2a-cli.git
   cd a2a-cli
   ```

2. **Create virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Test the installation:**
   ```bash
   python a2a_cli.py --help
   ```

### Method 2: Development Installation

If you want to modify the CLI or contribute to development:

1. **Clone and navigate:**
   ```bash
   git clone https://github.com/yourusername/a2a-cli.git
   cd a2a-cli
   ```

2. **Install in development mode:**
   ```bash
   pip install -e .
   ```

3. **Test installation:**
   ```bash
   a2a --help
   ```

### Method 3: Using setup.py

```bash
python setup.py install
```

## Verify Installation

Run the following commands to verify everything is working:

```bash
# Check CLI help
python a2a_cli.py --help

# Test connection (requires running A2A system)
python a2a_cli.py agents list
```

## Configuration

The CLI will automatically create a configuration file at `~/.a2a/config.json` with default settings:

```json
{
  "registry_url": "http://localhost:8000",
  "log_level": "INFO",
  "timeout": 30,
  "max_retries": 3,
  "output_format": "table"
}
```

You can modify these settings as needed.

## Running the A2A Multi-Agent System

Before using the CLI, make sure your A2A multi-agent system is running:

1. **Start the agent registry** (typically on port 8000)
2. **Launch your agents** (each on their own port)
3. **Verify agents are registered** using the CLI

## Troubleshooting

### Common Issues

1. **"Command not found" error:**
   - Make sure you're in the virtual environment
   - Try using `python a2a_cli.py` instead of `a2a`

2. **"Failed to connect to registry" error:**
   - Ensure your A2A multi-agent system is running
   - Check that the registry URL is correct in your config
   - Verify port 8000 is accessible

3. **Permission denied:**
   - On Unix systems, make the script executable: `chmod +x a2a_cli.py`

4. **Missing dependencies:**
   - Reinstall requirements: `pip install -r requirements.txt`

### Getting Help

- Check the main [README.md](README.md) for usage examples
- Run `python a2a_cli.py --help` for command help
- Use `python demo_cli.py` to test functionality

## Next Steps

After installation, check out:

- [README.md](README.md) - Complete usage guide
- [demo_cli.py](demo_cli.py) - Run demonstration script
- `python a2a_cli.py interactive` - Try interactive mode

## Updating

To update to the latest version:

```bash
git pull origin main
pip install -r requirements.txt
```

## Uninstalling

To remove the CLI:

```bash
# If installed with pip
pip uninstall a2a-cli

# If using virtual environment
rm -rf venv

# Remove configuration (optional)
rm -rf ~/.a2a
``` 