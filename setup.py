#!/usr/bin/env python3
"""
Setup script for A2A CLI
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="a2a-cli",
    version="1.0.0",
    author="A2A CLI Team",
    author_email="your-email@example.com",
    description="Advanced AI Agent Command Line Interface",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/a2a-cli",
    py_modules=["a2a_cli"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Systems Administration",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
    install_requires=[
        "click>=8.0.0",
        "requests>=2.28.0",
        "colorama>=0.4.0",
        "packaging>=21.0",
    ],
    entry_points={
        "console_scripts": [
            "a2a=a2a_cli:cli",
        ],
    },
    keywords="ai agents cli multi-agent mcp",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/a2a-cli/issues",
        "Source": "https://github.com/yourusername/a2a-cli",
        "Documentation": "https://github.com/yourusername/a2a-cli#readme",
    },
) 