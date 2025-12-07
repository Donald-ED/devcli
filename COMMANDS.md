# DevCLI Commands Reference

Quick reference for all available commands.

## Basic Commands

### Help & Version
```bash
devcli --help           # Show all commands
devcli --version        # Show version
devcli <command> --help # Help for specific command
```

### Test Command
```bash
devcli hello                    # Says hello!
devcli hello --name "YourName"  # Custom greeting
```

## Configuration Commands

### View Configuration
```bash
devcli config-show
```
Shows:
- Default model
- Max tokens setting
- All configured models
- Config file location

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
```

### Update Settings
```bash
devcli config-set <key> <value>
```

**Examples:**
```bash
# Change default model
devcli config-set default_model deepseek-r1

# Adjust token limit
devcli config-set max_tokens 4000
devcli config-set max_tokens 16000

# Any setting in config.json can be updated
```

### Add Models
```bash
devcli model-add <name> --provider <provider> --model <model-id> [--api-key <key>]
```

**Examples:**
```bash
# Add local Ollama models (no API key needed)
devcli model-add llama3 --provider ollama --model llama3.1
devcli model-add mistral --provider ollama --model mistral:7b
devcli model-add qwen --provider ollama --model qwen2.5:7b

# Add cloud models (API key required)
devcli model-add gpt4 --provider openai --model gpt-4 --api-key sk-...
devcli model-add claude --provider anthropic --model claude-4-opus --api-key sk-ant-...
```

## Coming Soon Commands

These are placeholders - functionality will be added soon!

### Initialize Project
```bash
devcli init
```
Will scan your project and build context.

### Ask Questions
```bash
devcli ask "your question here"
```
Will use AI to answer questions about your codebase.

**Examples:**
```bash
devcli ask "where is the authentication code?"
devcli ask "what does the main function do?"
devcli ask "how does the database connection work?"
```

### Execute Tasks
```bash
devcli task "description of what to do"
```
Will use AI to complete coding tasks.

**Examples:**
```bash
devcli task "add docstrings to all functions"
devcli task "refactor the error handling"
devcli task "add type hints to this file"
```

### Compare Models
```bash
devcli compare "question" --models model1,model2,model3
```
Will ask multiple models and compare responses.

## Config File Location

Your configuration is stored at:
- **Linux/Mac**: `~/.devcli/config.json`
- **Windows**: `C:\Users\YourName\.devcli\config.json`

You can edit this file directly if needed!

## Config File Structure

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

## Tips & Tricks

### Quick Setup for New User
```bash
# 1. Check current config
devcli config-show

# 2. Add your preferred models
devcli model-add my-llama --provider ollama --model llama3.1

# 3. Set as default
devcli config-set default_model my-llama

# 4. Done! Now when other commands work, they'll use this model
```

### Reset Config to Defaults
Just delete the config file and it will regenerate:
```bash
rm ~/.devcli/config.json
devcli config-show  # Creates fresh config
```

### Backup Your Config
```bash
cp ~/.devcli/config.json ~/devcli-config-backup.json
```

## Next Steps

1. ✅ You have config working
2. 🚧 Next: Connect to Ollama and make `ask` work
3. 🚧 Then: Add project scanning
4. 🚧 Then: Add agentic task execution

Stay tuned! 🚀