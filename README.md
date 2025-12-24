# DevCLI

> **The Free, Local-First AI Coding Assistant**
> 
> Claude Code's powerful interface + Free open-source models = DevCLI

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

---

## 🌟 What is DevCLI?

DevCLI brings AI-powered coding assistance to everyone - **completely free and private**. Unlike cloud-based alternatives, DevCLI runs entirely on your machine using local models via [Ollama](https://ollama.ai).

**The Best of Both Worlds:**
- Claude Code's intuitive chat interface ✨
- 100% free open-source models 🆓
- Complete privacy - never leaves your machine 🔒

---

## ✨ Key Features

### 🆓 **Completely Free**
No API costs, no subscriptions, no hidden fees. Use powerful models like DeepSeek, Llama, and Qwen without spending a dime.

### 🔒 **Privacy First**
Your code never leaves your machine. No telemetry, no tracking, no cloud uploads.

### 💬 **Interactive Chat Mode**
Just type `devcli` and start chatting - like Claude Code, but free!

### 🎯 **Project-Aware**
Understands your entire codebase. Get answers with specific file names and line numbers.

### 🤖 **Auto-Discovery**
Automatically finds and configures your Ollama models. No manual setup!

### 📊 **Three Output Modes**
- **Normal** - Beautiful, interactive
- **Quiet** - Clean, pipeable (`--quiet`)
- **JSON** - Structured, automatable (`--json`)

---

## 🚀 Quick Start

### Installation

```bash
# Install DevCLI
pip install devcli  # Coming to PyPI soon!

# Or install from source
git clone https://github.com/yourusername/devcli.git
cd devcli
pip install -e .
```

### Setup

```bash
# Install Ollama (if you haven't)
# Visit: https://ollama.ai

# Pull some models
ollama pull llama3.1
ollama pull deepseek-r1:7b

# Auto-discover models
devcli models-sync
```

### Start Chatting!

```bash
# Interactive mode (just type devcli!)
$ devcli

Welcome to DevCLI! 🤖
Model: llama3.1
Project context: ✓ loaded

> what does this project do?
[AI explains your project...]

> where is the authentication code?
[AI provides specific file paths...]

> exit
Goodbye! 👋
```

---

## 📖 Usage

### Interactive Mode (Recommended)

```bash
# Just type devcli to start chatting
devcli

# In-chat commands:
> /model deepseek-r1    # Switch models
> /nocontext           # Toggle project context
> /reset               # Clear history
> help                 # Show commands
> exit                 # Quit
```

### One-Shot Questions

```bash
# Normal mode
devcli ask "what does this project do?"

# With specific model
devcli ask "where is the auth logic?" --model deepseek-r1

# Without context (generic question)
devcli ask "explain async/await" --no-context
```

### Automation & Scripting

```bash
# Quiet mode - clean output for pipes
devcli ask "list all functions" --quiet | grep important

# JSON mode - structured data for scripts
devcli ask "analyze code" --json | jq '.response'

# Use in scripts
RESPONSE=$(devcli ask "check tests" --json | jq -r '.response')
echo "AI says: $RESPONSE"
```

### Project Understanding

```bash
# Scan your project
cd /path/to/your/project
devcli init

# Now ask context-aware questions
devcli ask "how does the config system work?"
# → AI responds with specific file names and line numbers!
```

---

## 🎯 Comparison

|  | DevCLI | Claudish | Claude Code | GitHub Copilot |
|---|:---:|:---:|:---:|:---:|
| **Cost** | 🆓 Free | 💰 API costs | 💰 $20/month | 💰 $10/month |
| **Privacy** | 🔒 100% local | ☁️ Cloud | ☁️ Cloud | ☁️ Cloud |
| **Dependencies** | ✅ Standalone | ❌ Needs Claude Code | ✅ Standalone | ❌ Needs IDE |
| **Models** | 🔓 Any Ollama model | 🔓 OpenRouter | 🔒 Anthropic only | 🔒 OpenAI only |
| **Interactive Chat** | ✅ Built-in | ❌ Via Claude Code | ✅ Yes | ❌ No |
| **Project Context** | ✅ Custom scan | ✅ Via Claude Code | ✅ Yes | ⚠️ Limited |
| **Offline** | ✅ Yes | ❌ No | ❌ No | ❌ No |
| **Auto-Discovery** | ✅ Yes | ❌ No | N/A | N/A |
| **JSON Output** | ✅ Yes | ✅ Yes | ❌ No | ❌ No |

---

## 📚 Commands

### Core Commands

```bash
devcli                          # Interactive chat (default!)
devcli ask "question"           # One-shot question
devcli init                     # Scan project
devcli models-sync              # Auto-discover models
```

### Configuration

```bash
devcli config-show              # View settings
devcli config-set key value     # Update setting
devcli model-add name --provider ollama --model llama3.1
```

### Output Modes

```bash
devcli ask "question"           # Normal (beautiful)
devcli ask "question" --quiet   # Quiet (pipeable)
devcli ask "question" --json    # JSON (automatable)
```

See [COMMANDS.md](COMMANDS.md) for complete reference.

---

## 🎨 Examples

### Example 1: Understand a New Codebase

```bash
$ cd unfamiliar-project/
$ devcli init
✓ Project initialized! 23 files scanned

$ devcli
> what does this project do?
[AI]: This is a REST API for task management built with FastAPI...

> where is the database connection code?
[AI]: The database connection is in `src/db/connection.py` lines 15-30...

> how does authentication work?
[AI]: Authentication uses JWT tokens. The logic is in:
      - `src/auth/jwt.py` (token generation)
      - `src/middleware/auth.py` (verification)
```

### Example 2: Automation

```bash
# Find all TODO comments
devcli ask "list all TODO comments" --quiet | grep -i urgent > urgent.txt

# Check test coverage
COVERAGE=$(devcli ask "analyze test coverage" --json | jq -r '.response')
if echo "$COVERAGE" | grep -q "low"; then
    echo "⚠️  Low test coverage detected!"
fi

# Generate documentation
for file in src/*.py; do
    devcli ask "document $file" --quiet >> DOCS.md
done
```

### Example 3: Multi-Model Comparison (Coming Soon)

```bash
# Try different models for the same task
devcli ask "optimize this function" --model llama3.1
devcli ask "optimize this function" --model deepseek-r1
devcli ask "optimize this function" --model qwen2.5

# Pick the best answer!
```

---

## 🏗️ Architecture

```
devcli/
├── cli.py              # Main CLI with Typer
├── config.py           # Configuration management (Pydantic)
├── core/
│   ├── scanner.py      # File scanning & filtering
│   └── context.py      # Project context building
└── providers/
    ├── base.py         # Provider interface
    └── ollama.py       # Ollama integration
```

**Tech Stack:**
- **CLI**: [Typer](https://typer.tiangolo.com/) - Modern CLI framework
- **UI**: [Rich](https://rich.readthedocs.io/) - Beautiful terminal output
- **Config**: [Pydantic](https://pydantic.dev/) - Type-safe configuration
- **Models**: [Ollama](https://ollama.ai) - Local LLM runtime

---

## 🗺️ Roadmap

### ✅ v0.1.0 - Foundation
- Project understanding & context
- Ollama integration
- Configuration system
- Auto-discovery

### ✅ v0.2.0 - Interactive
- Interactive chat mode
- Model switching
- Conversation history

### ✅ v0.3.0 - Polish (Current)
- JSON output mode
- Quiet mode
- Professional documentation
- MIT License

### 🚧 v0.4.0 - Advanced (Next)
- Status line (model/cost/context)
- Debug logging
- Token usage tracking
- Streaming responses

### 🔮 v0.5.0 - Power Features
- Code editing
- Model comparison
- OpenRouter integration
- RAG with embeddings

### 🎯 v1.0.0 - Production
- PyPI release
- CI/CD pipeline
- Comprehensive tests
- 1000+ GitHub stars

---

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

**Ways to contribute:**
- 🐛 Report bugs
- 💡 Suggest features
- 📖 Improve documentation
- 🔧 Submit pull requests
- ⭐ Star the repo!

---

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgments

**Inspired by:**
- [Claude Code](https://www.anthropic.com/claude-code) - Brilliant UX and agentic workflows
- [Claudish](https://github.com/MadAppGang/claudish) - JSON output and quiet mode ideas
- [Aider](https://github.com/paul-gauthier/aider) - Pioneering AI pair programming
- [Ollama](https://ollama.ai) - Making local LLMs accessible

**Built with:**
- [Typer](https://typer.tiangolo.com/) - CLI framework
- [Rich](https://rich.readthedocs.io/) - Terminal UI
- [Pydantic](https://pydantic.dev/) - Data validation

---

## 🌟 Star History

Star the repo to support development! ⭐

---

## 📞 Support

- 📖 [Documentation](COMMANDS.md)
- 🐛 [Issues](https://github.com/yourusername/devcli/issues)
- 💬 [Discussions](https://github.com/yourusername/devcli/discussions)
- 🐦 [Twitter](https://twitter.com/yourusername)

---

<div align="center">

**Made with ❤️ by developers, for developers**

[Get Started](SETUP.md) · [Documentation](COMMANDS.md) · [Contributing](CONTRIBUTING.md)

</div>
