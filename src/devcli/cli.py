"""
DevCLI - Main CLI Entry Point

This is where all the magic starts! When you type 'devcli' in your terminal,
Python runs this file.
"""
import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from devcli import __version__
from devcli import config

# Create the main Typer app
# Typer is a library that makes building CLIs super easy
app = typer.Typer(
    name="devcli",
    help="🚀 An open-source AI coding assistant that works with any LLM",
    add_completion=False,  # We don't need shell completion yet
)

# Rich makes our terminal output beautiful with colors and formatting
console = Console()


def version_callback(value: bool) -> None:
    """
    This function runs when someone types: devcli --version

    The 'callback' pattern is common in CLI tools - it's a function
    that gets called when a flag is used.
    """
    if value:
        console.print(f"[bold blue]DevCLI[/bold blue] version [green]{__version__}[/green]")
        raise typer.Exit()


@app.callback()
def main(
    version: bool = typer.Option(
        None,
        "--version",
        "-v",
        help="Show version and exit",
        callback=version_callback,
        is_eager=True,  # Run this before other commands
    ),
) -> None:
    """
    DevCLI - Your AI coding companion for free! 🤖

    This is the main callback that runs for every command.
    Think of it as the "entry point" before specific commands run.
    """
    pass


@app.command()
def hello(
    name: str = typer.Option("World", "--name", "-n", help="Who to greet")
) -> None:
    """
    Say hello! This is just a test command to make sure everything works.

    Try it:
      devcli hello
      devcli hello --name Alice
    """
    # Panel creates a nice box around our text
    console.print(
        Panel(
            f"[bold green]Hello, {name}![/bold green]\n\n"
            "🎉 DevCLI is working! You're ready to start building.\n\n"
            f"Version: [cyan]{__version__}[/cyan]",
            title="[bold blue]DevCLI[/bold blue]",
            border_style="blue",
        )
    )


@app.command()
def init() -> None:
    """
    Initialize DevCLI in your project (coming soon!)

    This will eventually:
    - Scan your project files
    - Build a context understanding
    - Set up configuration
    """
    console.print("[yellow]⚠️  Init command coming soon![/yellow]")
    console.print("\nWhat it will do:")
    console.print("  • Scan your project structure")
    console.print("  • Index your codebase")
    console.print("  • Set up local config")


@app.command()
def ask(question: str = typer.Argument(..., help="Your question about the codebase")) -> None:
    """
    Ask a question about your codebase (coming soon!)

    Example:
      devcli ask "where is the authentication code?"
    """
    console.print(f"[yellow]⚠️  You asked:[/yellow] {question}")
    console.print("[yellow]⚠️  Ask command coming soon![/yellow]")
    console.print("\nWhat it will do:")
    console.print("  • Understand your question")
    console.print("  • Search your codebase")
    console.print("  • Use AI to answer")


@app.command()
def config_show() -> None:
    """
    Show current configuration.

    Displays all your settings from ~/.devcli/config.json
    """
    cfg = config.get_config()

    # Create a nice table to show the config
    table = Table(title="DevCLI Configuration", show_header=True)
    table.add_column("Setting", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("Default Model", cfg.default_model)
    table.add_row("Max Tokens", str(cfg.max_tokens))
    table.add_row("Available Models", ", ".join(cfg.models.keys()))
    table.add_row("Config File", str(config.CONFIG_FILE))

    console.print(table)

    # Show detailed model info
    console.print("\n[bold]Model Details:[/bold]")
    for name, model_cfg in cfg.models.items():
        console.print(f"  [cyan]{name}[/cyan]: {model_cfg.provider}/{model_cfg.model_name}")


@app.command()
def config_set(
    key: str = typer.Argument(..., help="Config key to set (e.g., default_model, max_tokens)"),
    value: str = typer.Argument(..., help="New value")
) -> None:
    """
    Update a configuration value.

    Examples:
      devcli config-set default_model deepseek-r1
      devcli config-set max_tokens 4000
    """
    try:
        # Try to convert to int if it looks like a number
        if value.isdigit():
            config.update_config(**{key: int(value)})
        else:
            config.update_config(**{key: value})

        console.print(f"[green]✓[/green] Updated {key} = {value}")
        console.print(f"\n[dim]Config saved to: {config.CONFIG_FILE}[/dim]")

    except Exception as e:
        console.print(f"[red]✗[/red] Error: {e}")


@app.command()
def model_add(
    name: str = typer.Argument(..., help="Friendly name for the model"),
    provider: str = typer.Option(..., "--provider", "-p", help="Provider (ollama, openai, etc)"),
    model_name: str = typer.Option(..., "--model", "-m", help="Actual model identifier"),
    api_key: str = typer.Option(None, "--api-key", "-k", help="API key if needed")
) -> None:
    """
    Add a new model to your configuration.

    Example:
      devcli model-add my-llama --provider ollama --model llama3.1
      devcli model-add gpt4 --provider openai --model gpt-4 --api-key sk-...
    """
    try:
        config.add_model(name, provider, model_name, api_key)
        console.print(f"[green]✓[/green] Added model: {name}")
        console.print(f"  Provider: {provider}")
        console.print(f"  Model: {model_name}")

    except Exception as e:
        console.print(f"[red]✗[/red] Error: {e}")


# This is the actual entry point when you run 'devcli' command
# It's defined in pyproject.toml as: devcli = "devcli.cli:app"
if __name__ == "__main__":
    app()