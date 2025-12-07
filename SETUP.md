# Setup Guide: Getting DevCLI Working with Ollama

## What You Just Built

DevCLI is now **fully functional** and ready to talk to AI models! 🎉

You have:
- ✅ Working CLI with multiple commands
- ✅ Configuration system
- ✅ Ollama integration
- ✅ Beautiful terminal output
- ✅ Error handling

## To Use It On Your Machine:

### Step 1: Extract the Project
```bash
tar -xzf devcli.tar.gz
cd devcli
```

### Step 2: Set Up Python Environment
```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Install DevCLI
pip install -e .
```

### Step 3: Install Ollama

**Download and install from: https://ollama.ai**

- **Mac**: Download .dmg and install
- **Linux**: `curl -fsSL https://ollama.com/install.sh | sh`
- **Windows**: Download installer from website

### Step 4: Start Ollama & Pull Models

```bash
# Start Ollama (may start automatically on Mac/Windows)
ollama serve

# In another terminal, pull some models:
ollama pull llama3.1        # ~4.7GB, good all-rounder
ollama pull deepseek-r1:7b  # ~4.5GB, great at reasoning
ollama pull qwen2.5:7b      # ~4.5GB, multilingual

# Smaller/faster options:
ollama pull llama3.2:1b     # ~1.3GB, very fast
ollama pull phi3:mini       # ~2.3GB, from Microsoft
```

### Step 5: Configure DevCLI

```bash
# DevCLI auto-creates config on first run
devcli config-show

# Models are pre-configured! Just make sure they match what you pulled:
devcli model-add llama3 --provider ollama --model llama3.1
devcli config-set default_model llama3
```

### Step 6: Start Asking Questions!

```bash
# Basic usage
devcli ask "What is Python?"
devcli ask "Explain Docker in simple terms"
devcli ask "What is 2+2?"

# Use specific model
devcli ask "Write a hello world in Python" --model deepseek-r1
devcli ask "Explain async/await" --model llama3

# Ask anything!
devcli ask "How do I center a div in CSS?"
devcli ask "Explain quantum computing to a 10 year old"
devcli ask "Write a haiku about programming"
```

## See It In Action (Demo)

Want to see what it looks like before installing Ollama?

```bash
cd devcli
source venv/bin/activate
python demo_output.py
```

This shows simulated responses so you know what to expect!

## Troubleshooting

### "Cannot connect to Ollama"
- Make sure Ollama is installed
- Make sure it's running: `ollama serve`
- Check it's accessible: `curl http://localhost:11434`

### "Model not found"
- Pull the model: `ollama pull llama3.1`
- Check available models: `ollama list`
- Make sure model name in config matches: `devcli config-show`

### Import errors
- Make sure venv is activated: `source venv/bin/activate`
- Reinstall: `pip install -e .`

## What's Next?

Now that ask works, you can add:

1. **Project Understanding**
   - Scan local files
   - Build context about codebase
   - Ask questions about YOUR code

2. **Code Editing**
   - `devcli task "add docstrings"`
   - Actually modify files

3. **Multi-Model Comparison**
   - Ask 3 models the same question
   - Compare responses

4. **Streaming Responses**
   - See answers being generated in real-time
   - More interactive feel

## Commands Reference

```bash
# Help
devcli --help
devcli ask --help

# Config
devcli config-show
devcli config-set key value
devcli model-add name --provider ollama --model model-id

# Ask (the fun part!)
devcli ask "your question"
devcli ask "question" --model model-name

# Coming soon
devcli init                    # Scan project
devcli task "do something"     # Execute tasks
devcli compare "question"      # Compare models
```

## Tips

- **Start with small models** (llama3.2:1b) if you have limited RAM
- **Use specific models** for specific tasks:
  - `llama3.1` - General purpose, good at everything
  - `deepseek-r1` - Best for reasoning, math, code
  - `qwen2.5` - Great for non-English languages
- **Check model size** before pulling: `ollama show llama3.1`
- **GPU helps** but isn't required (CPU works, just slower)

## System Requirements

- **RAM**: 8GB minimum, 16GB+ recommended
- **Disk**: ~5GB per model
- **CPU**: Any modern processor
- **GPU**: Optional (NVIDIA, AMD, or Metal on Mac)

## Have Fun! 🚀

You built a real AI coding assistant from scratch! 

Try asking it programming questions, explanations, or even creative tasks. The models are surprisingly capable!

Questions? Check:
- README.md - Project overview
- LEARNING.md - Educational deep dive
- COMMANDS.md - Quick reference
- demo_output.py - See what it looks like
