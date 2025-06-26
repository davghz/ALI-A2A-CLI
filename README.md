# A2A CLI - Advanced AI Agent Command Line Interface

A comprehensive command-line tool for interacting with the A2A (Agent-to-Agent) multi-agent system and leveraging MCP (Model Context Protocol) tools.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## Features

- 🤖 **Agent Management**: List, monitor, and interact with AI agents
- 📊 **Health Monitoring**: Real-time agent health and performance metrics
- 🎯 **Task Submission**: Submit tasks to orchestrator or specific agents
- 🔧 **MCP Tools Integration**: Access Model Context Protocol tools
- 💬 **Interactive Mode**: Conversational interface for natural interaction
- ⚙️ **Configuration Management**: Persistent settings and preferences
- 🎨 **Beautiful CLI**: Colored output with intuitive formatting

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/a2a-cli.git
cd a2a-cli
```

2. Create a virtual environment (recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Make the CLI executable (Unix/Linux/macOS):
```bash
chmod +x a2a_cli.py
```

## Quick Start

### 1. Start the A2A Multi-Agent System

Before using the CLI, make sure your A2A multi-agent system is running with the agent registry on `http://localhost:8000`.

### 2. List Available Agents

```bash
python a2a_cli.py agents list
```

### 3. Check Agent Health

```bash
python a2a_cli.py agents status --detailed
```

### 4. Submit a Task

```bash
python a2a_cli.py task submit "Create a fibonacci function in Python"
```

### 5. Interactive Mode

```bash
python a2a_cli.py interactive
```

## Usage Guide

### Agent Commands

#### List Agents
```bash
# Table format (default)
python a2a_cli.py agents list

# JSON format
python a2a_cli.py agents list --format json
```

#### Check Agent Status
```bash
# Basic health check
python a2a_cli.py agents status

# Detailed health information
python a2a_cli.py agents status --detailed
```

#### Get Agent Information
```bash
python a2a_cli.py agents info OrchestratorAgent
```

### Task Management

#### Submit to Orchestrator
```bash
# Submit and wait for completion
python a2a_cli.py task submit "Your task here" --wait

# Submit with custom timeout
python a2a_cli.py task submit "Your task here" --wait --timeout 600
```

#### Submit to Specific Agent
```bash
# Submit to a specific agent
python a2a_cli.py task submit-to CodeBuilderAgent "Create a REST API" --wait
```

#### Check Task Status
```bash
python a2a_cli.py task status <task_id> <agent_endpoint>
```

### MCP Tools

#### List Available Tools
```bash
python a2a_cli.py mcp list
```

### Configuration

The CLI stores configuration in `~/.a2a/config.json`. Default settings:

```json
{
  "registry_url": "http://localhost:8000",
  "log_level": "INFO",
  "timeout": 30,
  "max_retries": 3,
  "output_format": "table"
}
```

## Examples

### Basic Workflow

```bash
# 1. Check if agents are running
python a2a_cli.py agents status

# 2. Submit a coding task
python a2a_cli.py task submit "Create a Python class for managing user accounts" --wait

# 3. Get detailed info about an agent
python a2a_cli.py agents info DeepseekChatV3Agent

# 4. Use interactive mode for ongoing conversations
python a2a_cli.py interactive
```

### Advanced Usage

```bash
# Submit task to specific agent and monitor
python a2a_cli.py task submit-to QwenCoderAgent "Optimize this SQL query: SELECT * FROM users" --wait

# Get agent list in JSON for scripting
python a2a_cli.py agents list --format json | jq '.[] | .name'

# Check detailed health with all metrics
python a2a_cli.py agents status --detailed
```

## Interactive Mode Commands

When in interactive mode, you can use these commands:

- `agents list` - List all agents
- `agents status` - Check agent health
- `task submit <prompt>` - Submit task to orchestrator
- `mcp list` - List MCP tools
- `help` - Show available commands
- `exit` or `quit` - Exit interactive mode

## Logging

Logs are automatically created in the `logs/` directory with the format `a2a_cli_YYYYMMDD.log`.

## Error Handling

The CLI includes comprehensive error handling:

- Network connectivity issues
- Agent unavailability
- Task submission failures
- Configuration problems

All errors are logged and displayed with helpful messages.

## Configuration Options

| Setting | Default | Description |
|---------|---------|-------------|
| `registry_url` | `http://localhost:8000` | URL of the agent registry |
| `log_level` | `INFO` | Logging level (DEBUG, INFO, WARNING, ERROR) |
| `timeout` | `30` | Request timeout in seconds |
| `max_retries` | `3` | Maximum retry attempts |
| `output_format` | `table` | Default output format |

## Troubleshooting

### Common Issues

1. **"Failed to connect to registry"**
   - Ensure the A2A multi-agent system is running
   - Check if port 8000 is accessible
   - Verify the registry URL in configuration

2. **"Agent not found"**
   - Run `python a2a_cli.py agents list` to see available agents
   - Check agent name spelling

3. **"Task submission failed"**
   - Verify agent health with `python a2a_cli.py agents status`
   - Check agent logs for errors

### Debug Mode

Enable debug logging:
```bash
# Set log level to DEBUG in config
python a2a_cli.py agents list  # Debug info will be in logs/
```

## Development

### Project Structure

```
a2a-cli/
├── a2a_cli.py           # Main CLI application
├── requirements.txt     # Python dependencies
├── README.md           # This file
├── LICENSE             # License file
├── .gitignore          # Git ignore patterns
├── demo_cli.py         # Demo script
├── logs/               # Log files (created automatically)
└── tools/              # MCP tools (if available)
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- 📧 **Issues**: Report bugs and request features via GitHub Issues
- 📚 **Documentation**: Check this README and inline help (`--help`)
- 💬 **Discussions**: Use GitHub Discussions for questions

## Changelog

### v1.0.0
- Initial release
- Full agent management capabilities
- Task submission and monitoring
- MCP tools integration
- Interactive mode
- Configuration management
- Comprehensive logging

---

Built with ❤️ for the A2A multi-agent ecosystem 