# DevCLI 🚀

An open-source AI coding assistant that brings Claude Code's powerful workflow to **free, open-source models**.

## Why DevCLI?

- 🆓 **100% Free** - Use local models via Ollama, no API costs
- 🔓 **Model Agnostic** - Switch between DeepSeek, Llama, Qwen, Mistral, and more
- 🧠 **Deep Context** - Understands your entire codebase
- 🤖 **Agentic Workflows** - Plans and executes multi-step coding tasks
- 🔒 **Privacy First** - Works completely offline
- 📊 **Smart Routing** - Automatically picks the best model for each task

## Quick Start

```bash
# Install
pip install -e .

# Initialize in your project
cd your-project/
devcli init

# Ask about your codebase
devcli ask "what does this project do?"

# Execute a coding task
devcli task "add error handling to the API endpoints"

# Compare responses from multiple models
devcli compare "explain this function" --models deepseek-r1,llama3.1
```

## Features

### 🎯 Current (v0.1.0)
- [x] Beautiful terminal UI with Rich
- [x] Configuration system (save/load settings)
- [x] Model management (add/configure models)
- [x] Config file at `~/.devcli/config.json`

### 🚧 In Progress
- [ ] Ollama integration (connect to local models)
- [ ] Basic question answering
- [ ] Project initialization and context building
- [ ] Agentic task planning and execution
- [ ] Code editing capabilities
- [ ] Semantic code search with embeddings
- [ ] Model performance tracking
- [ ] Git integration

### 🔮 Planned
- [ ] Parallel model execution
- [ ] Learning system (tracks best models per task)
- [ ] IDE extensions
- [ ] Team collaboration features

## Installation

### Prerequisites
- Python 3.10 or higher
- [Ollama](https://ollama.ai) (for local models)

### Install DevCLI
```bash
git clone https://github.com/yourusername/devcli.git
cd devcli
pip install -e .
```

### Setup Models
```bash
# Pull some models via Ollama
ollama pull llama3.1
ollama pull deepseek-r1:7b
ollama pull qwen2.5:7b
```

## Usage

### View Configuration
```bash
# See your current settings
devcli config-show

# Your config is stored at ~/.devcli/config.json
```

### Configure Models
```bash
# Add a new model
devcli model-add llama3 --provider ollama --model llama3.1

# Add a model that needs an API key
devcli model-add gpt4 --provider openai --model gpt-4 --api-key sk-...

# Set default model
devcli config-set default_model llama3

# Adjust token limit
devcli config-set max_tokens 4000
```

### Initialize in Your Project (Coming Soon)
```bash
cd your-project/
devcli init
```

This will scan your project and build an understanding of your codebase.

### Ask Questions (Coming Soon)
```bash
devcli ask "where is the authentication logic?"
devcli ask "what does the main function do?"
```

### Execute Tasks (Coming Soon)
```bash
devcli task "add docstrings to all functions in utils.py"
devcli task "refactor the database connection code"
```

### Compare Models (Coming Soon)
```bash
devcli compare "explain this bug" --models deepseek-r1,llama3.1,qwen2.5
```

## Configuration

DevCLI stores configuration in `~/.devcli/config.json`

```json
{
  "default_model": "deepseek-r1",
  "models": {
    "deepseek-r1": {
      "provider": "ollama",
      "model_name": "deepseek-r1:7b"
    },
    "llama3.1": {
      "provider": "ollama", 
      "model_name": "llama3.1"
    }
  },
  "context": {
    "max_files": 50,
    "max_tokens_per_file": 2000
  }
}
```

## Architecture

```
devcli/
├── cli.py              # CLI entry point
├── core/
│   ├── context.py      # Project understanding & context management
│   ├── models.py       # Model interface & routing
│   ├── planner.py      # Task planning (agentic workflows)
│   └── executor.py     # Task execution & code editing
├── providers/
│   ├── base.py         # Base provider interface
│   ├── ollama.py       # Ollama integration
│   └── litellm.py      # LiteLLM for API models
├── indexers/
│   ├── code_indexer.py # Semantic search with embeddings
│   └── file_watcher.py # Track file changes
└── utils/
    ├── file_utils.py   # File operations
    └── parser.py       # Code parsing
```

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Inspiration

DevCLI is inspired by:
- [Claude Code](https://www.anthropic.com/claude-code) - Amazing UX and agentic workflows
- [Aider](https://github.com/paul-gauthier/aider) - Pioneering AI pair programming
- [Continue.dev](https://continue.dev) - Open-source IDE extension

## License

MIT License - see [LICENSE](LICENSE) for details

## Roadmap

See our [GitHub Projects](https://github.com/yourusername/devcli/projects) for detailed roadmap.

**Star ⭐ the repo if you find this useful!**