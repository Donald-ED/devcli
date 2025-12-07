"""
DevCLI - Main CLI Entry Point

This is where all the magic starts! When you type 'devcli' in your terminal,
Python runs this file.
"""
import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.markdown import Markdown
from devcli import __version__
from devcli import config
from devcli.providers.ollama import OllamaProvider

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
def ask(
    question: str = typer.Argument(..., help="Your question"),
    model: str = typer.Option(None, "--model", "-m", help="Model to use (defaults to config)")
) -> None:
    """
    Ask a question and get an AI response!
    
    Example:
      devcli ask "What is Python?"
      devcli ask "Explain Docker in simple terms" --model deepseek-r1
    """
    # Get config to find model details
    cfg = config.get_config()
    
    # Determine which model to use
    model_name = model or cfg.default_model
    
    if model_name not in cfg.models:
        console.print(f"[red]✗[/red] Model '{model_name}' not found in config")
        console.print(f"[dim]Available models: {', '.join(cfg.models.keys())}[/dim]")
        console.print(f"\n[yellow]Tip:[/yellow] Add it with:")
        console.print(f"  devcli model-add {model_name} --provider ollama --model {model_name}")
        return
    
    model_cfg = cfg.models[model_name]
    
    # Only Ollama is supported for now
    if model_cfg.provider != "ollama":
        console.print(f"[red]✗[/red] Provider '{model_cfg.provider}' not supported yet")
        console.print("[yellow]Currently only 'ollama' provider is supported[/yellow]")
        return
    
    # Create provider
    provider = OllamaProvider(model_cfg.model_name)
    
    # Check if Ollama is running
    if not provider.is_available():
        console.print("[red]✗[/red] Cannot connect to Ollama!")
        console.print("\n[yellow]Make sure Ollama is installed and running:[/yellow]")
        console.print("  1. Install from: https://ollama.ai")
        console.print("  2. Start it: ollama serve")
        console.print(f"  3. Pull model: ollama pull {model_cfg.model_name}")
        return
    
    # Show what we're doing
    console.print(f"[dim]Using model: {model_name} ({model_cfg.model_name})[/dim]")
    console.print()
    
    # Ask the question with a spinner
    with console.status(f"[bold blue]Thinking...", spinner="dots"):
        try:
            response = provider.chat(
                message=question,
                system_prompt="You are a helpful AI assistant. Be concise and clear."
            )
        except Exception as e:
            console.print(f"[red]✗[/red] Error: {e}")
            return
    
    # Display the response in a nice panel
    console.print(
        Panel(
            Markdown(response),
            title=f"[bold blue]{model_name}[/bold blue]",
            border_style="blue",
        )
    )


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


@app.command()
def models_sync() -> None:
    """
    Auto-discover Ollama models and add them to your config.

    This will query Ollama for all installed models and automatically
    add any missing ones to your DevCLI configuration.

    Example:
      devcli models-sync
    """
    try:
        # Get list of Ollama models
        console.print("[dim]Querying Ollama for installed models...[/dim]")
        ollama_models = OllamaProvider.list_models()

        if not ollama_models:
            console.print("[yellow]No models found in Ollama[/yellow]")
            console.print("\n[dim]Pull some models first:[/dim]")
            console.print("  ollama pull llama3.1")
            console.print("  ollama pull deepseek-r1:7b")
            return

        # Get current config
        cfg = config.get_config()

        # Track what we add
        added = []
        skipped = []

        # Check each Ollama model
        for model in ollama_models:
            model_name = model['name']

            # Create a friendly name (remove :latest suffix if present)
            friendly_name = model_name.replace(':latest', '')

            # Check if already in config
            if friendly_name in cfg.models:
                skipped.append(friendly_name)
                continue

            # Add to config
            config.add_model(
                name=friendly_name,
                provider="ollama",
                model_name=model_name,
                api_key=None
            )
            added.append(friendly_name)

        # Show results
        console.print()
        if added:
            console.print(f"[green]✓[/green] Added {len(added)} new model(s):")
            for name in added:
                console.print(f"  • {name}")

        if skipped:
            console.print(f"\n[dim]Skipped {len(skipped)} existing model(s):[/dim]")
            for name in skipped:
                console.print(f"  • {name}")

        if not added:
            console.print("[green]✓[/green] All Ollama models are already in your config!")

        console.print(f"\n[dim]Total models in config: {len(cfg.models) + len(added)}[/dim]")

    except ConnectionError as e:
        console.print(f"[red]✗[/red] {e}")
    except Exception as e:
        console.print(f"[red]✗[/red] Error: {e}")


# This is the actual entry point when you run 'devcli' command
# It's defined in pyproject.toml as: devcli = "devcli.cli:app"
if __name__ == "__main__":
    app()
