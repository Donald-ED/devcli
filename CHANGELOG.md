# Changelog

All notable changes to DevCLI will be documented in this file.

## [0.3.1] - 2024-12-24

### Added
- **`/models` command** - List all available models in interactive mode
- **Better system prompt** - Significantly reduced hallucination

### Fixed
- AI hallucination issues (was making up code/libraries that don't exist)
- Missing `/models` command in help text
- System prompt now explicitly tells AI to stay grounded in project context

### Changed
- Welcome panel now shows `/models` command
- Help command now includes `/models`
- System prompt is much more careful and accurate

## [0.3.0] - 2024-12-24

### Added - Polish & Claudish-Inspired Features ✨
- **JSON output mode** (`--json`) - Structured output for automation and scripting
- **Quiet mode** (`--quiet`) - Clean output perfect for piping to other tools
- **Three output modes** for different use cases:
  - Normal: Beautiful, interactive (default)
  - Quiet: Clean, pipeable (`--quiet`)
  - JSON: Structured, automatable (`--json`)
- **LICENSE file** - MIT License
- **CHANGELOG.md** - This file!
- **demo_output_modes.py** - Demo showing new output modes

### Changed
- `ask` command now supports `--json` and `--quiet` flags
- Better output control for automation workflows
- Improved documentation

### Inspired By
- Claudish's JSON output mode for tool integration
- Claudish's quiet mode for clean pipeable output

## [0.2.0] - 2024-12-23

### Added
- **Interactive mode as default** - Just type `devcli` to start chatting
- **In-chat commands** - `/model`, `/nocontext`, `/reset`, `help`, `clear`, `exit`
- **Project context auto-loading** - Automatically uses `.devcli/context.json` if available
- **Model switching in chat** - Change models without leaving interactive mode
- **Conversation history tracking** - Foundation for future features
- **Beautiful welcome panel** - Shows model, context status, and available commands
- **Graceful exit handling** - Ctrl+C shows helpful message, EOF exits cleanly

### Changed
- Default behavior is now interactive mode (not one-shot)
- Improved error messages with helpful suggestions
- Better formatting of AI responses with Markdown rendering

### Fixed
- Edge case handling for empty inputs
- Proper cleanup on exit

## [0.1.0] - 2024-12-23

### Added
- **Project understanding** - Scan codebase and provide context-aware answers
- **Auto-discovery** - `models-sync` command to find Ollama models automatically
- **Configuration system** - Type-safe config with Pydantic
- **Ollama integration** - Chat with any local Ollama model
- **File scanning** - Smart filtering of code files
- **Context building** - Generate AI-friendly project summaries
- **Multiple commands**:
  - `init` - Scan project
  - `ask` - Ask questions (with/without context)
  - `config-show` - View settings
  - `config-set` - Update settings
  - `model-add` - Add models manually
  - `models-sync` - Auto-discover models
  - `hello` - Test command
- **Beautiful CLI** - Rich terminal formatting
- **Comprehensive documentation**:
  - README.md - Project overview
  - SETUP.md - Installation guide
  - COMMANDS.md - Quick reference
  - LEARNING.md - Educational content
  - FEATURES.md - Feature list

### Technical
- Python 3.8+ support
- Typer for CLI framework
- Rich for terminal UI
- Pydantic for configuration
- Requests for HTTP
- Type hints throughout
- Professional error handling

## [0.0.1] - 2024-12-23

### Added
- Initial project setup
- Basic CLI structure
- Hello world command
- Version command

---

## Upcoming Features

### v0.4.0 (Next)
- [ ] Status line with model/cost/context (like Claudish)
- [ ] Debug logging (`--debug`)
- [ ] Token usage display
- [ ] Cost tracking
- [ ] First-run tutorial

### v0.5.0 (Future)
- [ ] Streaming responses
- [ ] Code editing
- [ ] Model comparison
- [ ] OpenRouter integration

### v1.0.0 (Stable)
- [ ] All core features stable
- [ ] Published to PyPI
- [ ] Comprehensive tests
- [ ] Production-ready
