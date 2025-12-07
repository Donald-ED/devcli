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
from pathlib import Path
from devcli import __version__
from devcli import config
from devcli.providers.ollama import OllamaProvider
from devcli.core.context import ContextBuilder

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
def init(
    path: Path = typer.Argument(
        None,
        help="Project path (defaults to current directory)"
    ),
    force: bool = typer.Option(False, "--force", "-f", help="Reinitialize if already done")
) -> None:
    """
    Initialize DevCLI in your project.
    
    This scans your project files and builds an understanding
    that can be used when asking questions.
    
    Example:
      devcli init
      devcli init /path/to/project
      devcli init --force  # Re-scan
    """
    # Use current directory if not specified
    project_path = path or Path.cwd()
    project_path = project_path.resolve()
    
    # Check if path exists
    if not project_path.exists():
        console.print(f"[red]✗[/red] Path does not exist: {project_path}")
        return
    
    if not project_path.is_dir():
        console.print(f"[red]✗[/red] Path is not a directory: {project_path}")
        return
    
    # Check if already initialized
    context_file = project_path / ".devcli" / "context.json"
    if context_file.exists() and not force:
        console.print(f"[yellow]⚠️  Project already initialized![/yellow]")
        console.print(f"[dim]Context file: {context_file}[/dim]")
        console.print("\n[dim]Use --force to re-scan[/dim]")
        return
    
    console.print(f"\n[bold blue]Initializing DevCLI in:[/bold blue] {project_path}")
    console.print()
    
    # Build context
    with console.status("[bold blue]Scanning project files...", spinner="dots"):
        try:
            builder = ContextBuilder(project_path)
            context = builder.build_context(max_files=100)
        except Exception as e:
            console.print(f"[red]✗[/red] Error scanning project: {e}")
            return
    
    # Save context
    context_dir = project_path / ".devcli"
    context_dir.mkdir(exist_ok=True)
    
    try:
        builder.save_context(context, context_file)
    except Exception as e:
        console.print(f"[red]✗[/red] Error saving context: {e}")
        return
    
    # Show results
    console.print("[green]✓[/green] Project initialized successfully!\n")
    
    table = Table(show_header=False, box=None)
    table.add_column("Label", style="cyan")
    table.add_column("Value", style="green")
    
    table.add_row("Project", context.name)
    table.add_row("Files scanned", str(context.total_files))
    table.add_row("Lines of code", f"{context.total_lines:,}")
    table.add_row("Context saved", str(context_file))
    
    console.print(table)
    
    console.print("\n[dim]Now you can ask questions about your code:[/dim]")
    console.print('  devcli ask "what does this project do?"')
    console.print('  devcli ask "where is the main logic?"')


@app.command()
def ask(
    question: str = typer.Argument(..., help="Your question"),
    model: str = typer.Option(None, "--model", "-m", help="Model to use (defaults to config)"),
    no_context: bool = typer.Option(False, "--no-context", help="Don't use project context")
) -> None:
    """
    Ask a question and get an AI response!
    
    If you've run 'devcli init', this will include your project
    context when answering questions.
    
    Example:
      devcli ask "What is Python?"
      devcli ask "What does this project do?"
      devcli ask "Where is the authentication logic?"
      devcli ask "Explain Docker" --no-context
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
    
    # Try to load project context
    project_context = None
    if not no_context:
        context_file = Path.cwd() / ".devcli" / "context.json"
        if context_file.exists():
            try:
                builder = ContextBuilder(Path.cwd())
                project_context = builder.load_context(context_file)
                console.print(f"[dim]Using project context ({project_context.total_files} files)[/dim]")
            except Exception as e:
                console.print(f"[yellow]⚠️  Could not load project context: {e}[/yellow]")
    
    # Build the full question with context
    if project_context:
        # Create context-aware prompt
        context_prompt = project_context.to_prompt(max_tokens=cfg.max_tokens // 2)
        full_question = f"""{context_prompt}

---

User Question: {question}

Please answer based on the project context above when relevant."""
    else:
        full_question = question
    
    # Show what we're doing
    console.print(f"[dim]Using model: {model_name} ({model_cfg.model_name})[/dim]")
    console.print()
    
    # Ask the question with a spinner
    with console.status(f"[bold blue]Thinking...", spinner="dots"):
        try:
            response = provider.chat(
                message=full_question,
                system_prompt="You are a helpful AI coding assistant. Be concise and clear. When answering questions about code, provide specific file names and line numbers when possible."
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
