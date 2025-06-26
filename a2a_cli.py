#!/usr/bin/env python3
"""
A2A CLI - Advanced AI Agent Command Line Interface

A comprehensive CLI tool for interacting with the multi-agent system
and leveraging MCP (Model Context Protocol) tools.
"""

import click
import requests
import json
import os
import sys
import time
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from colorama import init, Fore, Back, Style
import threading
from concurrent.futures import ThreadPoolExecutor

# Initialize colorama for cross-platform colored output
init(autoreset=True)

# Configuration
DEFAULT_CONFIG = {
    "registry_url": "http://localhost:8000",
    "log_level": "INFO",
    "timeout": 30,
    "max_retries": 3,
    "output_format": "table"
}

class A2AConfig:
    """Configuration manager for A2A CLI"""
    
    def __init__(self):
        self.config_dir = Path.home() / ".a2a"
        self.config_file = self.config_dir / "config.json"
        self.config_dir.mkdir(exist_ok=True)
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file or create default"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    return {**DEFAULT_CONFIG, **json.load(f)}
            except Exception as e:
                click.echo(f"{Fore.YELLOW}Warning: Could not load config file: {e}")
        return DEFAULT_CONFIG.copy()
    
    def save_config(self):
        """Save current configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            click.echo(f"{Fore.RED}Error saving config: {e}")
    
    def get(self, key: str, default=None):
        """Get configuration value"""
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any):
        """Set configuration value"""
        self.config[key] = value
        self.save_config()

class A2AClient:
    """Client for interacting with the A2A multi-agent system"""
    
    def __init__(self, config: A2AConfig):
        self.config = config
        self.registry_url = config.get("registry_url")
        self.timeout = config.get("timeout", 30)
        self.session = requests.Session()
        self.session.timeout = self.timeout
        
        # Setup logging
        self._setup_logging()
    
    def _setup_logging(self):
        """Setup logging configuration"""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        log_file = log_dir / f"a2a_cli_{datetime.now().strftime('%Y%m%d')}.log"
        
        logging.basicConfig(
            level=getattr(logging, self.config.get("log_level", "INFO")),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def get_agents(self) -> List[Dict[str, Any]]:
        """Get list of available agents"""
        try:
            response = self.session.get(f"{self.registry_url}/agents")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            self.logger.error(f"Failed to get agents: {e}")
            raise click.ClickException(f"Failed to connect to registry: {e}")
    
    def get_agent_health(self, endpoint: str) -> Dict[str, Any]:
        """Get health status of a specific agent"""
        try:
            response = self.session.get(f"{endpoint}/health")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def submit_task(self, endpoint: str, prompt: str, data=None) -> Dict[str, Any]:
        """Submit a task to an agent"""
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
    
    def get_task_status(self, endpoint: str, task_id: str) -> Dict[str, Any]:
        """Get status of a specific task"""
        try:
            response = self.session.get(f"{endpoint}/task/{task_id}/status")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            self.logger.error(f"Failed to get task status: {e}")
            raise click.ClickException(f"Failed to get task status: {e}")

# Global configuration and client
config = A2AConfig()
client = A2AClient(config)

def print_table(headers: List[str], rows: List[List[str]], title: str = None):
    """Print a formatted table"""
    if title:
        click.echo(f"\n{Fore.CYAN}{Style.BRIGHT}{title}{Style.RESET_ALL}")
        click.echo("=" * len(title))
    
    if not rows:
        click.echo(f"{Fore.YELLOW}No data to display")
        return
    
    # Calculate column widths
    col_widths = [len(header) for header in headers]
    for row in rows:
        for i, cell in enumerate(row):
            if i < len(col_widths):
                col_widths[i] = max(col_widths[i], len(str(cell)))
    
    # Print headers
    header_row = " | ".join(f"{header:<{col_widths[i]}}" for i, header in enumerate(headers))
    click.echo(f"{Fore.GREEN}{Style.BRIGHT}{header_row}{Style.RESET_ALL}")
    click.echo("-" * len(header_row))
    
    # Print rows
    for row in rows:
        formatted_row = " | ".join(f"{str(cell):<{col_widths[i]}}" for i, cell in enumerate(row))
        click.echo(formatted_row)

@click.group()
@click.version_option(version="1.0.0")
def cli():
    """
    A2A CLI - Advanced AI Agent Command Line Interface
    
    A comprehensive tool for interacting with the multi-agent system
    and leveraging MCP (Model Context Protocol) tools.
    """
    pass

@cli.group()
def agents():
    """Manage and interact with AI agents"""
    pass

@agents.command("list")
@click.option("--format", type=click.Choice(["table", "json"]), default="table", help="Output format")
def list_agents(format):
    """List all available agents and their capabilities"""
    try:
        agents_data = client.get_agents()
        
        if format == "json":
            click.echo(json.dumps(agents_data, indent=2))
            return
        
        headers = ["Name", "Endpoint", "Status"]
        rows = []
        
        for agent in agents_data:
            status = agent.get("status", "unknown")
            rows.append([
                agent.get("name", "Unknown"),
                agent.get("endpoint", "Unknown"),
                f"{Fore.GREEN}Active{Style.RESET_ALL}" if status == "active" else f"{Fore.RED}{status}{Style.RESET_ALL}"
            ])
        
        print_table(headers, rows, f"Available Agents ({len(agents_data)})")
        
    except Exception as e:
        click.echo(f"{Fore.RED}Error: {e}")

@agents.command("status")
@click.option("--detailed", is_flag=True, help="Show detailed health information")
def agents_status(detailed):
    """Check health status of all agents"""
    try:
        agents_data = client.get_agents()
        
        headers = ["Name", "Endpoint", "Status", "CPU %", "Memory %"]
        if detailed:
            headers.extend(["Uptime", "Tasks Active"])
        
        rows = []
        
        for agent in agents_data:
            try:
                health = client.get_agent_health(agent["endpoint"])
                status = health.get("status", "unknown")
                status_color = Fore.GREEN if status == "healthy" else Fore.RED
                
                row = [
                    agent.get("name", "Unknown"),
                    agent.get("endpoint", "Unknown"),
                    f"{status_color}{status}{Style.RESET_ALL}",
                    f"{health.get('cpu_percent', 0):.1f}",
                    f"{health.get('memory_percent', 0):.1f}"
                ]
                
                if detailed:
                    row.extend([
                        health.get("uptime", "Unknown"),
                        str(health.get("active_tasks", 0))
                    ])
                
                rows.append(row)
                
            except Exception as e:
                row = [
                    agent.get("name", "Unknown"),
                    agent.get("endpoint", "Unknown"),
                    f"{Fore.RED}Error{Style.RESET_ALL}",
                    "N/A", "N/A"
                ]
                if detailed:
                    row.extend(["N/A", "N/A"])
                rows.append(row)
        
        print_table(headers, rows, "Agent Health Status")
        
    except Exception as e:
        click.echo(f"{Fore.RED}Error: {e}")

@agents.command("info")
@click.argument("agent_name")
def agent_info(agent_name):
    """Get detailed information about a specific agent"""
    try:
        agents_data = client.get_agents()
        agent = next((a for a in agents_data if a.get("name") == agent_name), None)
        
        if not agent:
            click.echo(f"{Fore.RED}Agent '{agent_name}' not found")
            return
        
        click.echo(f"\n{Fore.CYAN}{Style.BRIGHT}Agent Information: {agent_name}{Style.RESET_ALL}")
        click.echo("=" * 40)
        
        for key, value in agent.items():
            if isinstance(value, (list, dict)):
                value = json.dumps(value, indent=2)
            click.echo(f"{Fore.GREEN}{key}:{Style.RESET_ALL} {value}")
        
        # Get health information
        try:
            health = client.get_agent_health(agent["endpoint"])
            click.echo(f"\n{Fore.CYAN}Health Status:{Style.RESET_ALL}")
            for key, value in health.items():
                click.echo(f"  {key}: {value}")
        except Exception as e:
            click.echo(f"{Fore.YELLOW}Could not get health info: {e}")
            
    except Exception as e:
        click.echo(f"{Fore.RED}Error: {e}")

@cli.group()
def task():
    """Manage tasks and submissions"""
    pass

@task.command("submit")
@click.argument("prompt")
@click.option("--wait", is_flag=True, help="Wait for task completion")
@click.option("--timeout", default=300, help="Timeout for waiting (seconds)")
def submit_task(prompt, wait, timeout):
    """Submit a task to the orchestrator agent"""
    try:
        # Find orchestrator agent
        agents_data = client.get_agents()
        orchestrator = next((a for a in agents_data if "orchestrator" in a.get("name", "").lower()), None)
        
        if not orchestrator:
            click.echo(f"{Fore.RED}Orchestrator agent not found")
            return
        
        click.echo(f"{Fore.CYAN}Submitting task to orchestrator...")
        task_data = client.submit_task(orchestrator["endpoint"], prompt)
        task_id = task_data.get("task_id")
        
        click.echo(f"{Fore.GREEN}Task submitted successfully!")
        click.echo(f"Task ID: {task_id}")
        click.echo(f"Endpoint: {orchestrator['endpoint']}")
        
        if wait:
            click.echo(f"{Fore.CYAN}Waiting for completion (timeout: {timeout}s)...")
            
            start_time = time.time()
            while time.time() - start_time < timeout:
                status = client.get_task_status(orchestrator["endpoint"], task_id)
                state = status.get("state")
                
                if state == "completed":
                    click.echo(f"{Fore.GREEN}Task completed successfully!")
                    if status.get("outputs"):
                        click.echo(f"{Fore.CYAN}Results:")
                        for output in status["outputs"]:
                            click.echo(f"  {output.get('content', '')}")
                    return
                elif state == "failed":
                    click.echo(f"{Fore.RED}Task failed!")
                    if status.get("outputs"):
                        click.echo(f"{Fore.YELLOW}Error details:")
                        for output in status["outputs"]:
                            click.echo(f"  {output.get('content', '')}")
                    return
                elif state == "pending":
                    click.echo(f"{Fore.YELLOW}Task still pending...")
                
                time.sleep(2)
            
            click.echo(f"{Fore.YELLOW}Timeout reached. Task may still be running.")
            click.echo(f"Use 'python cli/a2a_cli.py task status {task_id} {orchestrator['endpoint']}' to check progress.")
            
    except Exception as e:
        click.echo(f"{Fore.RED}Error: {e}")

@task.command("submit-to")
@click.argument("agent_name")
@click.argument("prompt")
@click.option("--wait", is_flag=True, help="Wait for task completion")
def submit_to_agent(agent_name, prompt, wait):
    """Submit a task to a specific agent"""
    try:
        agents_data = client.get_agents()
        agent = next((a for a in agents_data if a.get("name") == agent_name), None)
        
        if not agent:
            click.echo(f"{Fore.RED}Agent '{agent_name}' not found")
            return
        
        click.echo(f"{Fore.CYAN}Submitting task to {agent_name}...")
        task_data = client.submit_task(agent["endpoint"], prompt)
        task_id = task_data.get("task_id")
        
        click.echo(f"{Fore.GREEN}Task submitted successfully!")
        click.echo(f"Task ID: {task_id}")
        click.echo(f"Endpoint: {agent['endpoint']}")
        
        if wait:
            click.echo(f"{Fore.CYAN}Waiting for completion...")
            start_time = time.time()
            while time.time() - start_time < 300:  # 5 minute timeout
                status = client.get_task_status(agent["endpoint"], task_id)
                state = status.get("state")
                
                if state == "completed":
                    click.echo(f"{Fore.GREEN}Task completed successfully!")
                    if status.get("outputs"):
                        click.echo(f"{Fore.CYAN}Results:")
                        for output in status["outputs"]:
                            click.echo(f"  {output.get('content', '')}")
                    return
                elif state == "failed":
                    click.echo(f"{Fore.RED}Task failed!")
                    if status.get("outputs"):
                        click.echo(f"{Fore.YELLOW}Error details:")
                        for output in status["outputs"]:
                            click.echo(f"  {output.get('content', '')}")
                    return
                
                time.sleep(2)
            
    except Exception as e:
        click.echo(f"{Fore.RED}Error: {e}")

@task.command("status")
@click.argument("task_id")
@click.argument("agent_endpoint")
def task_status_cmd(task_id, agent_endpoint):
    """Check the status of a task"""
    try:
        status = client.get_task_status(agent_endpoint, task_id)
        
        click.echo(f"\n{Fore.CYAN}Task Status: {task_id}{Style.RESET_ALL}")
        click.echo("=" * 40)
        
        state = status.get("state", "unknown")
        state_color = Fore.GREEN if state == "completed" else Fore.YELLOW if state == "pending" else Fore.RED
        
        click.echo(f"State: {state_color}{state}{Style.RESET_ALL}")
        click.echo(f"Agent: {status.get('handled_by', 'Unknown')}")
        
        if status.get("outputs"):
            click.echo(f"\n{Fore.CYAN}Outputs:{Style.RESET_ALL}")
            for i, output in enumerate(status["outputs"]):
                click.echo(f"  {i+1}. {output.get('content', '')}")
                
    except Exception as e:
        click.echo(f"{Fore.RED}Error: {e}")

@cli.group()
def mcp():
    """Work with MCP (Model Context Protocol) tools"""
    pass

@mcp.command("list")
def list_mcp_tools():
    """List available MCP tools"""
    tools_dir = Path("tools")
    if not tools_dir.exists():
        click.echo(f"{Fore.RED}Tools directory not found")
        return
    
    click.echo(f"{Fore.CYAN}Available MCP Tools:{Style.RESET_ALL}")
    click.echo("=" * 20)
    
    for tool_file in tools_dir.glob("*.py"):
        if tool_file.name != "__init__.py":
            click.echo(f"  📁 {tool_file.stem}")

@cli.command("interactive")
def interactive_mode():
    """Start interactive conversation mode"""
    click.echo(f"{Fore.CYAN}Starting A2A Interactive Mode{Style.RESET_ALL}")
    click.echo("Type 'exit' to quit, 'help' for commands\n")
    
    while True:
        try:
            prompt = click.prompt(f"{Fore.GREEN}A2A", prompt_suffix="> ")
            
            if prompt.lower() in ['exit', 'quit']:
                click.echo(f"{Fore.CYAN}Goodbye!")
                break
            elif prompt.lower() == 'help':
                click.echo(f"{Fore.CYAN}Available commands:")
                click.echo("  agents list - List all agents")
                click.echo("  agents status - Check agent health")
                click.echo("  task submit <prompt> - Submit task to orchestrator")
                click.echo("  mcp list - List MCP tools")
                click.echo("  exit - Exit interactive mode")
            else:
                # Default to submitting as a task
                submit_task.callback(prompt, wait=True, timeout=60)
                
        except KeyboardInterrupt:
            click.echo(f"\n{Fore.CYAN}Goodbye!")
            break
        except Exception as e:
            click.echo(f"{Fore.RED}Error: {e}")

if __name__ == "__main__":
    cli()
