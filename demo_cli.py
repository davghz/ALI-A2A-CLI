#!/usr/bin/env python3
"""
Demo script for A2A CLI

This script demonstrates the key features of the A2A CLI
by running through common usage scenarios.
"""

import subprocess
import time
import sys
from pathlib import Path

def run_command(cmd, description):
    """Run a CLI command and display the result"""
    print(f"\n{'='*60}")
    print(f"🚀 {description}")
    print(f"{'='*60}")
    print(f"Command: {cmd}")
    print("-" * 40)
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print(f"Stderr: {result.stderr}")
        return result.returncode == 0
    except Exception as e:
        print(f"Error running command: {e}")
        return False

def main():
    """Run the A2A CLI demo"""
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║              A2A CLI DEMONSTRATION                       ║
    ║                                                          ║
    ║  This demo shows the main features of the A2A CLI       ║
    ║  Make sure your A2A multi-agent system is running!      ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    # Check if CLI script exists
    cli_script = Path("a2a_cli.py")
    if not cli_script.exists():
        print(f"❌ CLI script not found: {cli_script}")
        print("Make sure you're in the correct directory!")
        sys.exit(1)
    
    # Demo commands
    demos = [
        {
            "cmd": "python a2a_cli.py --help",
            "desc": "Show CLI help and available commands"
        },
        {
            "cmd": "python a2a_cli.py agents list",
            "desc": "List all available agents"
        },
        {
            "cmd": "python a2a_cli.py agents status",
            "desc": "Check health status of all agents"
        },
        {
            "cmd": "python a2a_cli.py agents status --detailed",
            "desc": "Get detailed health information"
        },
        {
            "cmd": "python a2a_cli.py mcp list",
            "desc": "List available MCP tools"
        },
        {
            "cmd": "python a2a_cli.py task submit 'Create a simple fibonacci function in Python' --wait --timeout 60",
            "desc": "Submit a task to the orchestrator and wait for completion"
        }
    ]
    
    # Run demonstrations
    success_count = 0
    for demo in demos:
        if run_command(demo["cmd"], demo["desc"]):
            success_count += 1
        
        # Pause between commands
        time.sleep(2)
    
    # Summary
    print(f"\n{'='*60}")
    print(f"📊 DEMO SUMMARY")
    print(f"{'='*60}")
    print(f"Commands executed: {len(demos)}")
    print(f"Successful: {success_count}")
    print(f"Failed: {len(demos) - success_count}")
    
    if success_count == len(demos):
        print("\n🎉 All demonstrations completed successfully!")
        print("The A2A CLI is working properly.")
    else:
        print(f"\n⚠️  Some demonstrations failed.")
        print("Check that your A2A multi-agent system is running.")
    
    print(f"\n📚 For more information, run:")
    print(f"   python a2a_cli.py --help")
    print(f"   python a2a_cli.py interactive")

if __name__ == "__main__":
    main() 