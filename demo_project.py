#!/usr/bin/env python3
"""
Demo: Project-Aware Questions

Shows what DevCLI looks like when asking questions about YOUR code.
"""
import sys
sys.path.insert(0, 'src')

from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

console = Console()

print("\n" + "="*70)
print("🎭 DEMO: DevCLI with Project Understanding")
print("="*70 + "\n")

# Simulate: devcli init
console.print("[bold cyan]$ devcli init[/bold cyan]\n")
console.print("[dim]Scanning project files...[/dim]\n")
console.print("[green]✓[/green] Project initialized successfully!\n")
console.print("[cyan]Project[/cyan]        devcli")
console.print("[cyan]Files scanned[/cyan]  20")
console.print("[cyan]Lines of code[/cyan]  2,531\n")

print("-"*70 + "\n")

# Example 1: Ask about the project
console.print("[bold cyan]$ devcli ask \"what does this project do?\"[/bold cyan]")
console.print("[dim]Using project context (20 files)[/dim]")
console.print("[dim]Using model: llama3.1[/dim]\n")

response1 = """**DevCLI** is an open-source AI coding assistant that brings Claude Code's workflow to free, local LLM models.

**Core Features:**
- **Multi-model support**: Works with any Ollama model (Llama, DeepSeek, Qwen, etc.)
- **Configuration system**: Saves preferences in `~/.devcli/config.json`
- **Project understanding**: Scans codebases and provides context-aware answers
- **Beautiful CLI**: Built with Typer and Rich for great UX

**Main Components:**
- `cli.py` - Command-line interface with commands like `ask`, `init`, `config-show`
- `config.py` - Configuration management with Pydantic
- `providers/ollama.py` - Integration with local Ollama models
- `core/scanner.py` & `core/context.py` - Project file scanning and context building

The goal is to provide a free alternative to paid AI coding assistants like GitHub Copilot or Claude Code."""

console.print(
    Panel(
        Markdown(response1),
        title="[bold blue]llama3.1[/bold blue]",
        border_style="blue",
    )
)

print("\n" + "-"*70 + "\n")

# Example 2: Ask specific code question
console.print("[bold cyan]$ devcli ask \"how does the config system work?\"[/bold cyan]")
console.print("[dim]Using project context (20 files)[/dim]")
console.print("[dim]Using model: deepseek-r1[/dim]\n")

response2 = """The configuration system is implemented in **`src/devcli/config.py`** using Pydantic for type-safe data management.

**Key Components:**

1. **Config Models** (lines 13-58):
   - `ModelConfig`: Stores provider, model_name, and optional API key
   - `Config`: Main config with default_model, models dict, max_tokens, and ignore patterns

2. **Storage** (lines 61-63):
   - Location: `~/.devcli/config.json`
   - Created automatically on first run

3. **Core Functions**:
   - `load_config()`: Reads JSON, validates with Pydantic, returns Config object
   - `save_config()`: Converts Config to dict and writes to JSON
   - `add_model()`: Adds new model to config
   - `update_config()`: Updates specific settings

4. **Default Config** (lines 79-95):
   - Includes llama3.1 and deepseek-r1 by default
   - Max 2000 tokens
   - Ignores common directories (node_modules, venv, etc.)

**CLI Integration**:
Commands like `config-show`, `config-set`, and `model-add` in `cli.py` use these functions to manage settings."""

console.print(
    Panel(
        Markdown(response2),
        title="[bold blue]deepseek-r1[/bold blue]",
        border_style="blue",
    )
)

print("\n" + "-"*70 + "\n")

# Example 3: Ask about specific file
console.print("[bold cyan]$ devcli ask \"what does scanner.py do?\"[/bold cyan]")
console.print("[dim]Using project context (20 files)[/dim]")
console.print("[dim]Using model: llama3.1[/dim]\n")

response3 = """**`src/devcli/core/scanner.py`** implements the file scanning functionality for project understanding.

**Purpose**: Walks through a project directory and finds all relevant code files while respecting ignore patterns.

**Key Class: FileScanner**

- **Supported file types** (lines 18-25): Python, JavaScript, TypeScript, Java, C/C++, Go, Rust, Ruby, PHP, HTML/CSS, config files, markdown, etc.

- **Ignored by default** (lines 28-36):
  - Directories: node_modules, venv, .git, __pycache__, dist, build
  - Files: *.pyc, *.min.js, .env, *.log

- **Main methods**:
  - `scan()`: Returns list of Path objects for all code files
  - `get_file_tree()`: Generates a visual tree representation
  - `should_ignore_dir()` & `should_ignore_file()`: Filter logic

**Usage**: The ContextBuilder in `context.py` uses FileScanner to find files before reading their contents."""

console.print(
    Panel(
        Markdown(response3),
        title="[bold blue]llama3.1[/bold blue]",
        border_style="blue",
    )
)

print("\n" + "="*70)
print("✨ This is DevCLI with project understanding!")
print("   It knows YOUR codebase and can answer specific questions.")
print("="*70 + "\n")
