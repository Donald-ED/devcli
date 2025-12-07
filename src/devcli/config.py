"""
Configuration Management for DevCLI

This module handles reading and writing the user's configuration file.
We use Pydantic for type safety - it's like TypeScript for Python!

Config file location: ~/.devcli/config.json
"""
from pathlib import Path
from typing import Dict, Optional
import json
from pydantic import BaseModel, Field


class ModelConfig(BaseModel):
    """
    Configuration for a single model.
    
    Pydantic automatically validates types and provides defaults.
    Think of this as a TypeScript interface but with runtime validation!
    """
    provider: str = Field(
        ...,  # Required field (the ... means "no default")
        description="Provider name (e.g., 'ollama', 'openai')"
    )
    model_name: str = Field(
        ..., 
        description="Actual model identifier (e.g., 'llama3.1', 'gpt-4')"
    )
    api_key: Optional[str] = Field(
        None,  # Optional field, defaults to None
        description="API key if needed for this provider"
    )


class Config(BaseModel):
    """
    Main configuration for DevCLI.
    
    This represents the entire config.json file structure.
    Pydantic will validate all fields when we load the config.
    """
    default_model: str = Field(
        "llama3.1",
        description="Default model to use when none specified"
    )
    models: Dict[str, ModelConfig] = Field(
        default_factory=dict,  # Empty dict by default
        description="Available models and their configurations"
    )
    max_tokens: int = Field(
        2000,
        description="Maximum tokens to send to models"
    )
    project_ignore: list[str] = Field(
        default_factory=lambda: [
            "node_modules",
            "venv",
            ".git",
            "__pycache__",
            "*.pyc",
            ".env"
        ],
        description="Files/folders to ignore when scanning projects"
    )


# This is where the config file lives
# Path.home() gets the user's home directory (~)
# We put our config in a hidden folder (~/.devcli/)
CONFIG_DIR = Path.home() / ".devcli"
CONFIG_FILE = CONFIG_DIR / "config.json"


def ensure_config_dir() -> None:
    """
    Create the config directory if it doesn't exist.
    
    mkdir_parents=True means "create parent directories too"
    exist_ok=True means "don't error if it already exists"
    """
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)


def get_default_config() -> Config:
    """
    Create a default configuration with sensible defaults.
    
    This is what new users get on first run.
    """
    return Config(
        default_model="llama3.1",
        models={
            "llama3.1": ModelConfig(
                provider="ollama",
                model_name="llama3.1"
            ),
            "deepseek-r1": ModelConfig(
                provider="ollama",
                model_name="deepseek-r1:7b"
            ),
        },
        max_tokens=2000
    )


def load_config() -> Config:
    """
    Load configuration from disk.
    
    If config doesn't exist, create default and save it.
    Returns: Config object with all settings
    """
    ensure_config_dir()
    
    if not CONFIG_FILE.exists():
        # First time user - create default config
        config = get_default_config()
        save_config(config)
        return config
    
    try:
        # Read the JSON file
        with open(CONFIG_FILE, 'r') as f:
            data = json.load(f)
        
        # Pydantic automatically validates and creates Config object
        # If the JSON doesn't match our schema, this will raise an error
        config = Config(**data)  # ** unpacks the dict into keyword arguments
        return config
        
    except Exception as e:
        # If config is corrupted, fall back to defaults
        print(f"Warning: Could not load config ({e}), using defaults")
        return get_default_config()


def save_config(config: Config) -> None:
    """
    Save configuration to disk.
    
    Args:
        config: Config object to save
    """
    ensure_config_dir()
    
    # Pydantic's model_dump() converts the object back to a dict
    # We can serialize to JSON
    data = config.model_dump()
    
    # Write with nice formatting (indent=2)
    with open(CONFIG_FILE, 'w') as f:
        json.dump(data, f, indent=2)


def get_config() -> Config:
    """
    Convenience function to get config.
    Most code should call this instead of load_config().
    """
    return load_config()


def update_config(**kwargs) -> Config:
    """
    Update specific config values and save.
    
    Example:
        update_config(default_model="deepseek-r1")
        update_config(max_tokens=4000)
    
    Returns: Updated config
    """
    config = load_config()
    
    # Update only the fields provided
    for key, value in kwargs.items():
        if hasattr(config, key):
            setattr(config, key, value)
    
    save_config(config)
    return config


def add_model(name: str, provider: str, model_name: str, api_key: Optional[str] = None) -> None:
    """
    Add a new model to the configuration.
    
    Args:
        name: Friendly name for the model (e.g., "my-llama")
        provider: Provider type (e.g., "ollama")
        model_name: Actual model identifier
        api_key: Optional API key
    """
    config = load_config()
    
    config.models[name] = ModelConfig(
        provider=provider,
        model_name=model_name,
        api_key=api_key
    )
    
    save_config(config)


# Example usage (if running this file directly):
if __name__ == "__main__":
    # Test the config system
    print("Testing config system...")
    
    config = get_config()
    print(f"Default model: {config.default_model}")
    print(f"Available models: {list(config.models.keys())}")
    print(f"Max tokens: {config.max_tokens}")
    
    # Try updating
    update_config(max_tokens=4000)
    print("Updated max_tokens to 4000")
    
    # Verify
    config = get_config()
    print(f"New max_tokens: {config.max_tokens}")
