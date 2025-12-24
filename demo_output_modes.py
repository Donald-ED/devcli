#!/usr/bin/env python3
"""
Demo: JSON Output Mode and Quiet Mode

Shows how DevCLI's new output modes work.
Inspired by Claudish!
"""
import sys
sys.path.insert(0, 'src')

from rich.console import Console
from rich.syntax import Syntax
import json

console = Console()

print("\n" + "="*70)
print("🎭 DEMO: JSON & Quiet Output Modes")
print("="*70 + "\n")

# Demo 1: Normal Mode
console.print("[bold cyan]1. Normal Mode (default)[/bold cyan]")
console.print("[dim]$ devcli ask \"what is 2+2?\"[/dim]\n")

console.print("[dim]Using model: llama3.1 (llama3.1)[/dim]")
console.print()
console.print("╭────────── llama3.1 ──────────╮")
console.print("│ 2 + 2 = 4                    │")
console.print("│                              │")
console.print("│ This is basic arithmetic.    │")
console.print("╰──────────────────────────────╯")

console.print("\n[dim]Perfect for interactive use![/dim]\n")

# Demo 2: Quiet Mode
console.print("\n[bold cyan]2. Quiet Mode (--quiet)[/bold cyan]")
console.print("[dim]$ devcli ask \"list 3 colors\" --quiet[/dim]\n")

console.print("1. Red")
console.print("2. Blue")  
console.print("3. Green")

console.print("\n[dim]Clean output, great for piping:[/dim]")
console.print("[dim]$ devcli ask \"list files\" --quiet | grep .py[/dim]\n")

# Demo 3: JSON Mode
console.print("\n[bold cyan]3. JSON Mode (--json)[/bold cyan]")
console.print("[dim]$ devcli ask \"what is Python?\" --json[/dim]\n")

json_output = {
    "question": "what is Python?",
    "response": "Python is a high-level programming language known for its simplicity and readability. Created by Guido van Rossum in 1991, it emphasizes code readability and allows programmers to express concepts in fewer lines of code.",
    "model": "llama3.1",
    "model_id": "llama3.1",
    "duration_ms": 1234,
    "context_used": False,
    "context_files": 0
}

syntax = Syntax(json.dumps(json_output, indent=2), "json", theme="monokai")
console.print(syntax)

console.print("\n[dim]Perfect for automation and scripting![/dim]\n")

# Demo 4: Automation Examples
console.print("\n[bold cyan]4. Automation Examples[/bold cyan]\n")

console.print("[bold]Extract just the response:[/bold]")
console.print('[dim]$ devcli ask "task" --json | jq -r \'.response\'[/dim]\n')

console.print("[bold]Get duration:[/bold]")
console.print('[dim]$ devcli ask "task" --json | jq \'.duration_ms\'[/dim]\n')

console.print("[bold]Check if context was used:[/bold]")
console.print('[dim]$ devcli ask "task" --json | jq \'.context_used\'[/dim]\n')

console.print("[bold]Use in scripts:[/bold]")
code = """RESPONSE=$(devcli ask "check tests" --json | jq -r '.response')
echo "AI says: $RESPONSE"

# Track files analyzed
FILES=$(devcli ask "task" --json | jq '.context_files')
echo "Analyzed $FILES files"
"""
syntax = Syntax(code.strip(), "bash", theme="monokai")
console.print(syntax)

print("\n" + "="*70)
print("✨ Three output modes for every use case!")
print("   • Normal: Beautiful, interactive")
print("   • Quiet: Clean, pipeable")  
print("   • JSON: Structured, automatable")
print("="*70 + "\n")
