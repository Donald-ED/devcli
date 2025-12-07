#!/usr/bin/env python3
"""
Test script to demonstrate what DevCLI looks like with working AI

This bypasses Ollama and shows you what the output would look like.
"""
import sys
sys.path.insert(0, 'src')

from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

console = Console()

print("\n" + "="*70)
print("🎭 DEMO: What DevCLI looks like with a working AI model")
print("="*70 + "\n")

# Simulate: devcli ask "What is Python?"
console.print("[bold cyan]$ devcli ask \"What is Python?\"[/bold cyan]")
console.print("[dim]Using model: llama3.1 (llama3.1)[/dim]\n")

response = """Python is a high-level, interpreted programming language known for its simplicity and readability. Created by Guido van Rossum in 1991, it emphasizes code readability with significant whitespace.

**Key Features:**
- **Easy to learn**: Clean syntax, great for beginners
- **Versatile**: Web dev, data science, AI, automation
- **Large ecosystem**: Thousands of libraries (NumPy, Django, etc.)
- **Cross-platform**: Runs on Windows, Mac, Linux

Python is used by companies like Google, Netflix, and NASA!"""

console.print(
    Panel(
        Markdown(response),
        title="[bold blue]llama3.1[/bold blue]",
        border_style="blue",
    )
)

print("\n" + "-"*70 + "\n")

# Simulate: devcli ask "What is 2+2?" --model deepseek-r1
console.print("[bold cyan]$ devcli ask \"What is 2+2?\" --model deepseek-r1[/bold cyan]")
console.print("[dim]Using model: deepseek-r1 (deepseek-r1:7b)[/dim]\n")

response2 = "2 + 2 = **4**\n\nThis is a basic arithmetic operation. Addition is one of the fundamental operations in mathematics."

console.print(
    Panel(
        Markdown(response2),
        title="[bold blue]deepseek-r1[/bold blue]",
        border_style="blue",
    )
)

print("\n" + "-"*70 + "\n")

# Simulate: devcli ask "Explain Docker simply"
console.print("[bold cyan]$ devcli ask \"Explain Docker simply\"[/bold cyan]")
console.print("[dim]Using model: llama3.1 (llama3.1)[/dim]\n")

response3 = """**Docker in Simple Terms:**

Imagine you're moving to a new apartment. Instead of packing individual items, you pack everything into a shipping container. That container can go anywhere - ship, truck, train - and everything inside stays organized.

Docker does the same for applications:
1. **Containers**: Package your app + all dependencies
2. **Portable**: Works the same on any computer
3. **Isolated**: Won't conflict with other apps
4. **Fast**: Starts in seconds, not minutes

**Example:** Your Python app needs specific libraries. Put it in a Docker container, and it'll work on your laptop, your friend's computer, and the production server - guaranteed!"""

console.print(
    Panel(
        Markdown(response3),
        title="[bold blue]llama3.1[/bold blue]",
        border_style="blue",
    )
)

print("\n" + "="*70)
print("✨ This is what DevCLI will look like on your machine!")
print("   Install Ollama and pull a model to see it work for real.")
print("="*70 + "\n")
