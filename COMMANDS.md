# DevCLI Commands Reference

Quick reference for all available commands in v0.3.0.

## 🚀 Interactive Mode (Default)

Just type `devcli` to start an interactive chat session!

```bash
$ devcli

Welcome to DevCLI! 🤖
Model: llama3.1 (llama3.1)
Project context: ✓ loaded

Commands:
  exit or quit - Exit chat
  clear - Clear screen
  help - Show help
  /model <n> - Switch model
  /nocontext - Toggle project context
  /reset - Reset conversation

Just type your question and press Enter!

> what does this project do?
[AI responds...]

> where is the auth code?
[AI responds...]

> exit
Goodbye! 👋
```

### In-Chat Commands

| Command | Description |
|---------|-------------|
| `exit`, `quit`, `q` | Exit interactive mode |
| `clear` | Clear the screen |
| `help` | Show available commands |
| `/model <n>` | Switch to different model |
| `/nocontext` | Toggle project context on/off |
| `/reset` | Clear conversation history |

---

## 📚 One-Shot Commands

### `ask` - Ask AI a Question

Ask a question and get an AI-powered answer. Automatically includes project context if available.

```bash
devcli ask "What is Python?"
devcli ask "What does this project do?"
devcli ask "Where is the authentication code?" --model deepseek-r1
devcli ask "Explain Docker" --no-context
```

#### Options

- `--model, -m <n>` - Use specific model (overrides default)
- `--no-context` - Don't include project context
- `--json` - Output in JSON format (for automation)
- `--quiet, -q` - Suppress informational messages

#### Output Modes

**Normal Mode (default):**
```bash
$ devcli ask "what is 2+2?"

Using model: llama3.1 (llama3.1)

╭────────── llama3.1 ──────────╮
│ 2 + 2 = 4                    │
│                              │
│ This is basic arithmetic.    │
╰──────────────────────────────╯
```

**Quiet Mode (`--quiet`):**
```bash
$ devcli ask "list 3 colors" --quiet
1. Red
2. Blue
3. Green
```
Perfect for piping: `devcli ask "list files" --quiet | grep .py`

**JSON Mode (`--json`):**
```bash
$ devcli ask "what is Python?" --json
{
  "question": "what is Python?",
  "response": "Python is a high-level programming language...",
  "model": "llama3.1",
  "model_id": "llama3.1",
  "duration_ms": 1234,
  "context_used": false,
  "context_files": 0
}
```
Perfect for automation: `devcli ask "task" --json | jq '.response'`

#### Examples

```bash
# Normal interactive use
devcli ask "How does this auth system work?"

# Pipe to other tools (quiet mode)
devcli ask "list all API endpoints" --quiet | grep POST

# Automation with JSON
RESPONSE=$(devcli ask "check tests" --json | jq -r '.response')
echo "AI says: $RESPONSE"

# Get metadata
devcli ask "analyze code" --json | jq '{model, duration_ms, context_files}'

# Use specific model
devcli ask "complex task" --model deepseek-r1
```

---

## 🔍 Project Commands

### `init` - Initialize Project

Scan your project and build context for AI-aware responses.

```bash
devcli init                    # Scan current directory
devcli init /path/to/project   # Scan specific path
devcli init --force            # Re-scan (update context)
```

**What it does:**
- Scans all code files in your project
- Ignores common directories (node_modules, venv, .git, etc.)
- Builds a context file at `.devcli/context.json`
- Enables context-aware AI responses

**Example output:**
```
✓ Project initialized successfully!

Project        my-app
Files scanned  23
Lines of code  3,456
Context saved  /path/to/project/.devcli/context.json

Now you can ask questions about your code:
  devcli ask "what does this project do?"
  devcli ask "where is the main logic?"
```

---

## ⚙️ Configuration Commands

### `config-show` - View Configuration

Display your current DevCLI configuration.

```bash
devcli config-show
```

**Example output:**
```
┏━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Setting          ┃ Value                 ┃
┡━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━┩
│ Default Model    │ llama3.1              │
│ Max Tokens       │ 8000                  │
│ Available Models │ llama3.1, deepseek-r1 │
└──────────────────┴───────────────────────┘

Model Details:
  llama3.1: ollama/llama3.1
  deepseek-r1: ollama/deepseek-r1:7b

Config: /home/user/.devcli/config.json
```

### `config-set` - Update Settings

Update configuration values.

```bash
devcli config-set <key> <value>
```

**Examples:**
```bash
# Change default model
devcli config-set default_model deepseek-r1

# Increase token limit
devcli config-set max_tokens 16000

# All settings are saved to ~/.devcli/config.json
```

**Available settings:**
- `default_model` - Default model to use
- `max_tokens` - Maximum tokens per request

---

## 🤖 Model Commands

### `model-add` - Add Model Manually

Add a new model to your configuration.

```bash
devcli model-add <n> --provider <p> --model <m> [--api-key <k>]
```

**Examples:**
```bash
# Add Ollama model
devcli model-add llama3 --provider ollama --model llama3.1

# Add another variant
devcli model-add deepseek --provider ollama --model deepseek-r1:7b

# For future: Add cloud model
devcli model-add gpt4 --provider openai --model gpt-4 --api-key sk-...
```

### `models-sync` - Auto-Discover Models

Automatically find and add all Ollama models.

```bash
devcli models-sync
```

**What it does:**
- Queries Ollama for installed models
- Adds any missing models to config
- Skips models already configured
- Shows what was added/skipped

**Example output:**
```
Querying Ollama for installed models...

✓ Added 3 new model(s):
  • llama3.1
  • deepseek-r1:7b
  • qwen2.5:7b

Skipped 1 existing model(s):
  • mistral

Total models in config: 4
```

---

## 🛠️ Utility Commands

### `hello` - Test Command

Verify DevCLI is working.

```bash
devcli hello                   # Default greeting
devcli hello --name "Alice"    # Custom name
```

### `--version` - Show Version

Display DevCLI version.

```bash
devcli --version
# DevCLI version 0.3.0
```

### `--help` - Show Help

Show all available commands.

```bash
devcli --help                  # All commands
devcli <command> --help        # Help for specific command
```

---

## 📁 Configuration File

Your configuration is stored at: `~/.devcli/config.json`

**Structure:**
```json
{
  "default_model": "llama3.1",
  "models": {
    "llama3.1": {
      "provider": "ollama",
      "model_name": "llama3.1",
      "api_key": null
    },
    "deepseek-r1": {
      "provider": "ollama",
      "model_name": "deepseek-r1:7b",
      "api_key": null
    }
  },
  "max_tokens": 8000,
  "project_ignore": [
    "node_modules",
    "venv",
    ".git",
    "__pycache__",
    "*.pyc",
    ".env"
  ]
}
```

You can edit this file directly if needed!

---

## 💡 Tips & Tricks

### Quick Setup for New Users

```bash
# 1. Check current config
devcli config-show

# 2. Auto-discover models
devcli models-sync

# 3. Initialize your project
cd /path/to/your/project
devcli init

# 4. Start chatting!
devcli
```

### Automation Workflows

```bash
# Get clean output for scripts
devcli ask "list all functions" --quiet

# JSON for structured data
devcli ask "analyze errors" --json | jq '.response'

# Pipe to other tools
devcli ask "show TODOs" --quiet | grep -i urgent

# Track metadata
devcli ask "review code" --json | jq '{duration_ms, context_files}'
```

### Model Management

```bash
# See what models you have
devcli config-show

# Add new models
devcli models-sync  # Auto-discover

# Or add manually
devcli model-add custom --provider ollama --model custom-model:tag

# Switch default
devcli config-set default_model custom
```

---

## 🎯 Complete Workflow Example

```bash
# Step 1: Set up DevCLI
cd ~/my-project
devcli models-sync              # Find available models
devcli config-show              # Check configuration

# Step 2: Initialize project
devcli init                     # Scan codebase

# Step 3: Interactive exploration
devcli                          # Start interactive mode
> what does this project do?
> where is the database code?
> how does authentication work?
> exit

# Step 4: One-shot queries
devcli ask "list all API endpoints" --quiet > endpoints.txt
devcli ask "find security issues" --json | jq '.response'

# Step 5: Automation
for file in *.py; do
  devcli ask "analyze $file" --quiet
done
```

---

## 📚 More Resources

- **README.md** - Project overview and features
- **SETUP.md** - Installation and setup guide
- **LEARNING.md** - Educational content and concepts
- **FEATURES.md** - Complete feature list
- **CHANGELOG.md** - Version history
