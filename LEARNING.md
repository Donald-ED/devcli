# Learning Guide: Your First CLI Tool 🎓

## What We Just Built

You now have a working CLI tool called `devcli`! Let's break down what each part does.

## Project Structure

```
devcli/
├── pyproject.toml          # Project configuration (like package.json for Node)
├── README.md               # Documentation
├── venv/                   # Virtual environment (Python's sandbox)
└── src/
    └── devcli/
        ├── __init__.py     # Makes this a Python package
        └── cli.py          # Main CLI code
```

## Key Concepts Explained

### 1. Virtual Environment (`venv/`)

**What is it?**
A virtual environment is like a separate installation of Python for your project. It keeps your project's dependencies isolated from other projects.

**Why do we need it?**
- Prevents version conflicts between projects
- Makes it easy to share exact dependencies
- Keeps your system Python clean

**Commands:**
```bash
# Create venv
python3 -m venv venv

# Activate it (Linux/Mac)
source venv/bin/activate
# Or
. venv/bin/activate

# Deactivate
deactivate
```

### 2. `pyproject.toml`

**What is it?**
The modern way to configure Python projects. It replaces old files like `setup.py` and `requirements.txt`.

**Key sections:**

```toml
[project]
name = "devcli"              # Package name
version = "0.1.0"            # Version number
dependencies = [             # Libraries we need
    "typer[all]>=0.9.0",
    "rich>=13.0.0",
]

[project.scripts]
devcli = "devcli.cli:app"    # Creates 'devcli' command
#        └─ module:variable  # Points to our app
```

### 3. `__init__.py`

**What is it?**
A special file that tells Python "this directory is a package".

**What's in it?**
```python
__version__ = "0.1.0"
```

We can import this elsewhere: `from devcli import __version__`

### 4. `cli.py` - The Main Code

Let's break down each part:

#### Import Section
```python
import typer                    # CLI framework
from rich.console import Console # Pretty terminal output
from rich.panel import Panel     # Boxes around text
```

#### Creating the App
```python
app = typer.Typer(
    name="devcli",
    help="🚀 Description",
)
```

This creates your CLI application. When you type `devcli --help`, Typer shows this description.

#### The Callback (Entry Point)
```python
@app.callback()
def main(...):
    pass
```

**What's a callback?**
A function that runs BEFORE any command. Think of it as the "setup" that happens every time.

**What's a decorator (`@app.callback()`)?**
The `@` symbol is a decorator - it's Python's way of wrapping a function with extra behavior. Here it tells Typer: "this is the main entry point".

#### Commands

```python
@app.command()
def hello(name: str = typer.Option("World", "--name", "-n")):
    console.print(f"Hello, {name}!")
```

**Breaking it down:**
- `@app.command()` - Makes this function a command
- `def hello(...)` - Command name (becomes `devcli hello`)
- `name: str` - Type hint (tells Python this is a string)
- `typer.Option(...)` - Makes this a flag option
  - `"World"` - Default value
  - `"--name"` - Long flag (`devcli hello --name Alice`)
  - `"-n"` - Short flag (`devcli hello -n Alice`)

#### Type Hints

```python
def hello(name: str) -> None:
    #           ^^^       ^^^^
    #           |         └─ Function returns nothing
    #           └─ Parameter is a string
```

Type hints help:
- Catch bugs before running
- Make code self-documenting
- Enable better IDE autocomplete

### 5. How It All Connects

1. You type: `devcli hello --name Alice`
2. Shell looks for `devcli` command
3. Finds it in `pyproject.toml`: points to `devcli.cli:app`
4. Python loads `devcli/cli.py`
5. Runs `app()` which is the Typer app
6. Typer sees "hello" and calls the `hello()` function
7. Typer sees `--name Alice` and passes `name="Alice"`
8. Function runs and prints output!

## Testing Your Changes

```bash
# Always activate venv first
. venv/bin/activate

# Install in "editable" mode (-e means changes reflect immediately)
pip install -e .

# Test it
devcli --help
devcli hello
devcli hello --name YourName
```

## Common Commands

```bash
# See what's installed in your venv
pip list

# Install a new dependency
pip install some-package

# Run your CLI
devcli <command>

# Exit venv when done
deactivate
```

## Next Steps

Now that you understand the basics, we can add:
1. ✅ Configuration file (save/load settings)
2. ✅ Connect to Ollama (talk to AI models)
3. ✅ Read files from your project
4. ✅ More complex commands

## Try This Yourself!

**Exercise 1:** Add a new command `goodbye`
```python
@app.command()
def goodbye(name: str = typer.Option("Friend", "--name", "-n")) -> None:
    """Say goodbye!"""
    console.print(f"[red]Goodbye, {name}! 👋[/red]")
```

**Exercise 2:** Add a flag to `hello` for enthusiasm level
```python
def hello(
    name: str = typer.Option("World", "--name", "-n"),
    excited: bool = typer.Option(False, "--excited", "-e", help="Add excitement!")
) -> None:
    """Say hello!"""
    greeting = f"Hello, {name}"
    if excited:
        greeting += "!!!! 🎉🎊🥳"
    else:
        greeting += "!"
    console.print(greeting)
```

Test: `devcli hello --name You --excited`

## Questions?

- **What's the difference between Argument and Option?**
  - Argument: Required, positional (`devcli ask "my question"`)
  - Option: Optional, has flag (`devcli hello --name Bob`)

- **Why `if __name__ == "__main__":`?**
  - Lets you run the file directly: `python cli.py`
  - But we use the `devcli` command instead (defined in pyproject.toml)

- **What's `Console()` from Rich?**
  - A nicer version of `print()` with colors, formatting, and styles

## What We've Built So Far

### ✅ Step 1: Basic CLI (Complete)
- Created project structure
- Set up Typer for commands
- Added version and help
- Made `devcli hello` work

### ✅ Step 2: Configuration System (Complete)
- **File**: `src/devcli/config.py`
- **Config location**: `~/.devcli/config.json`
- **Commands**:
  - `devcli config-show` - View settings
  - `devcli config-set key value` - Update settings
  - `devcli model-add name --provider X --model Y` - Add models

**Key concepts learned**:
- **Pydantic models** for type-safe configuration
- **JSON serialization** with `json.dump()` and `json.load()`
- **Path operations** with `pathlib.Path`
- **Rich Tables** for beautiful output
- **Optional types** with `Optional[str]`

**Example config file**:
```json
{
  "default_model": "llama3.1",
  "models": {
    "llama3.1": {
      "provider": "ollama",
      "model_name": "llama3.1",
      "api_key": null
    }
  },
  "max_tokens": 8000,
  "project_ignore": ["node_modules", "venv", ".git"]
}
```

### 🚧 Step 3: Ollama Integration (Next)
Connect to local AI models and make `devcli ask` actually work!

## Deep Dive: Understanding config.py

Let's break down the key parts:

### Pydantic Models

```python
class ModelConfig(BaseModel):
    provider: str = Field(..., description="Provider name")
    model_name: str = Field(..., description="Model identifier")
    api_key: Optional[str] = Field(None, description="API key")
```

**What's happening?**
- `BaseModel` - Makes this a Pydantic model (like TypeScript interface)
- `Field(...)` - Required field (no default)
- `Field(None)` - Optional field (defaults to None)
- `Optional[str]` - Can be string or None
- Pydantic validates types automatically!

### Reading/Writing JSON

```python
# Write
data = config.model_dump()  # Convert to dict
json.dump(data, f, indent=2)  # Save to file

# Read
data = json.load(f)  # Read from file
config = Config(**data)  # Convert to Pydantic model
```

The `**data` syntax "unpacks" the dict into keyword arguments.

### Path Operations

```python
CONFIG_DIR = Path.home() / ".devcli"
CONFIG_FILE = CONFIG_DIR / "config.json"

# Create directory
CONFIG_DIR.mkdir(parents=True, exist_ok=True)

# Check if exists
if CONFIG_FILE.exists():
    ...
```

**Why `Path` instead of strings?**
- Works on Windows, Mac, Linux
- `/` operator joins paths correctly
- Built-in methods like `.exists()`, `.mkdir()`

### Try It: Add a New Config Field

**Exercise**: Add a `verbose` boolean setting

1. Update the `Config` class in `config.py`:
```python
class Config(BaseModel):
    default_model: str = Field(...)
    models: Dict[str, ModelConfig] = Field(...)
    max_tokens: int = Field(2000)
    verbose: bool = Field(False, description="Enable verbose output")  # Add this!
    project_ignore: list[str] = Field(...)
```

2. Test it:
```bash
devcli config-show  # See verbose: False
devcli config-set verbose true
devcli config-show  # See verbose: True
```

## Resources

- [Typer Documentation](https://typer.tiangolo.com)
- [Rich Documentation](https://rich.readthedocs.io)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)

Ready for the next step? Let's add configuration support! 🚀
