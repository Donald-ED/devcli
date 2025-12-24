#!/usr/bin/env python3
"""
Demo: Fixed Hallucination & Added /models Command

Shows improvements to v0.3.1:
1. Better system prompt to reduce hallucination
2. New /models command to list available models
"""
import sys
sys.path.insert(0, 'src')

from rich.console import Console
from rich.panel import Panel

console = Console()

print("\n" + "="*70)
print("🎭 DEMO: v0.3.1 Fixes - Hallucination & /models Command")
print("="*70 + "\n")

# Demo 1: Welcome Panel (Now shows /models)
console.print("[bold cyan]1. Updated Welcome Panel[/bold cyan]\n")

console.print(Panel(
    f"[bold blue]Welcome to DevCLI![/bold blue] 🤖\n\n"
    f"Model: [cyan]llama3.1[/cyan] (llama3.1)\n"
    f"Project context: [cyan]✓ loaded[/cyan]\n\n"
    f"[dim]Commands:[/dim]\n"
    f"  [cyan]exit[/cyan] or [cyan]quit[/cyan] - Exit chat\n"
    f"  [cyan]clear[/cyan] - Clear screen\n"
    f"  [cyan]help[/cyan] - Show help\n"
    f"  [cyan]/model <n>[/cyan] - Switch model\n"
    f"  [cyan]/models[/cyan] - List available models [green]← NEW![/green]\n"
    f"  [cyan]/nocontext[/cyan] - Toggle project context\n"
    f"  [cyan]/reset[/cyan] - Reset conversation\n\n"
    f"Just type your question and press Enter!",
    title="[bold]DevCLI Interactive Chat[/bold]",
    border_style="blue"
))

console.print("\n[dim]Now users can see available models anytime![/dim]\n")

# Demo 2: /models command
console.print("\n[bold cyan]2. New /models Command[/bold cyan]\n")

console.print("[bold green]>[/bold green] /models\n")
console.print("[bold]Available Models:[/bold]\n")
console.print("  [cyan]llama3.1[/cyan] (llama3.1) ← current")
console.print("  [cyan]deepseek-r1[/cyan] (deepseek-r1:7b)")
console.print("  [cyan]qwen2.5[/cyan] (qwen2.5:7b)")
console.print("\n[dim]Use '/model <n>' to switch[/dim]\n")

console.print("\n[dim]Quick and easy model discovery![/dim]\n")

# Demo 3: Improved System Prompt
console.print("\n[bold cyan]3. Better System Prompt (Reduces Hallucination)[/bold cyan]\n")

console.print("[bold]Old System Prompt:[/bold]")
console.print('[dim]"You are a helpful AI coding assistant. Be concise and clear."[/dim]\n')

console.print("[bold]New System Prompt:[/bold]")
console.print('''[green]CRITICAL RULES:
- Only answer based on project files in context
- If not in context, say "I don't see that"  
- NEVER make up code or file paths
- Quote exact file paths when answering
- Be accurate - if unsure, say so[/green]
''')

console.print("\n[dim]Much more careful and grounded![/dim]\n")

# Demo 4: Before vs After
console.print("\n[bold cyan]4. Before vs After Examples[/bold cyan]\n")

console.print("[bold]❌ Before (Hallucinating):[/bold]")
console.print("[bold green]>[/bold green] what is the CLI doing at line 200?\n")
console.print('[red]"The CLI uses the click library... @click.command()..."[/red]')
console.print('[dim]^ Made up library that does not exist![/dim]\n')

console.print("[bold]✅ After (Truthful):[/bold]")
console.print("[bold green]>[/bold green] what is the CLI doing at line 200?\n")
console.print('[green]Looking at src/devcli/cli.py line 200:')
console.print('console = Console()')
console.print("Creates the Rich Console instance")
console.print('[dim]^ Accurate, from actual code![/dim]\n')

print("="*70)
print("✨ Fixes Applied!")
print("   • /models command added")
print("   • System prompt improved")
print("   • Hallucination reduced")
print("   • Better user experience")
print("="*70 + "\n")
