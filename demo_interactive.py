#!/usr/bin/env python3
"""
Demo: Interactive Chat Mode

Shows what DevCLI's interactive mode looks like.
"""
import sys

sys.path.insert(0, 'src')

from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
import time

console = Console()

print("\n" + "=" * 70)
print("🎭 DEMO: DevCLI Interactive Mode")
print("=" * 70 + "\n")

# Simulate starting interactive mode
console.print("[bold cyan]$ devcli[/bold cyan]\n")

time.sleep(0.5)

# Welcome message
console.print(Panel(
    f"[bold blue]Welcome to DevCLI![/bold blue] 🤖\n\n"
    f"Model: [cyan]llama3.1[/cyan] (llama3.1)\n"
    f"Project context: [cyan]✓ loaded[/cyan]\n\n"
    f"[dim]Commands:[/dim]\n"
    f"  [cyan]exit[/cyan] or [cyan]quit[/cyan] - Exit chat\n"
    f"  [cyan]clear[/cyan] - Clear screen\n"
    f"  [cyan]help[/cyan] - Show help\n"
    f"  [cyan]/model <name>[/cyan] - Switch model\n"
    f"  [cyan]/nocontext[/cyan] - Toggle project context\n\n"
    f"Just type your question and press Enter!",
    title="[bold]DevCLI Interactive Chat[/bold]",
    border_style="blue"
))
console.print()

# Simulate conversation
conversations = [
    {
        "user": "what does this project do?",
        "response": """**DevCLI** is an open-source AI coding assistant that works with free, local LLM models.

Key features:
- Works with Ollama (Llama, DeepSeek, Qwen, etc.)
- Understands your codebase via project scanning
- Interactive chat mode (what you're using now!)
- 100% free and runs locally"""
    },
    {
        "user": "how does the scanner work?",
        "response": """The scanner (`src/devcli/core/scanner.py`) walks through your project directory and finds code files.

**Key features:**
- Supports 20+ file types (Python, JS, Go, etc.)
- Ignores common directories (node_modules, venv, .git)
- Respects .gitignore-style patterns
- Filters by file size (skips huge files)

It returns a list of Path objects for all relevant code files."""
    },
    {
        "user": "/model deepseek-r1",
        "response": None,
        "system": "[green]✓[/green] Switched to model: deepseek-r1"
    },
    {
        "user": "what's 2+2?",
        "response": "2 + 2 = **4**\n\nThis is basic arithmetic addition."
    }
]

for conv in conversations:
    # User input
    console.print(f"[bold green]>[/bold green] {conv['user']}")
    time.sleep(0.3)

    if conv.get('system'):
        # System message
        console.print(f"\n{conv['system']}\n")
        time.sleep(0.3)
    elif conv['response']:
        # AI response
        console.print()
        console.print(Markdown(conv['response']))
        console.print()
        time.sleep(0.5)

# Exit
console.print("[bold green]>[/bold green] exit")
console.print("\n[cyan]Goodbye! 👋[/cyan]\n")

print("=" * 70)
print("✨ Interactive mode makes DevCLI feel like a real conversation!")
print("   Just type 'devcli' and start asking questions.")
print("=" * 70 + "\n")