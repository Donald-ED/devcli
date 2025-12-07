"""
Providers Package

This package contains integrations with different LLM providers:
- Ollama (local models)
- OpenAI (coming soon)
- Anthropic (coming soon)
- etc.
"""
from devcli.providers.base import BaseProvider
from devcli.providers.ollama import OllamaProvider

__all__ = ["BaseProvider", "OllamaProvider"]
