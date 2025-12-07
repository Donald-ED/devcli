"""
Base Provider Interface

All model providers (Ollama, OpenAI, etc.) will implement this interface.
This is like an "abstract class" or "interface" in other languages.
"""
from abc import ABC, abstractmethod
from typing import Optional


class BaseProvider(ABC):
    """
    Abstract base class for all LLM providers.
    
    ABC = Abstract Base Class (you can't create instances of this directly)
    Any provider must implement these methods.
    """
    
    def __init__(self, model_name: str, api_key: Optional[str] = None):
        """
        Initialize the provider.
        
        Args:
            model_name: The specific model to use (e.g., "llama3.1")
            api_key: Optional API key for cloud providers
        """
        self.model_name = model_name
        self.api_key = api_key
    
    @abstractmethod
    def chat(self, message: str, system_prompt: Optional[str] = None) -> str:
        """
        Send a message and get a response.
        
        Args:
            message: The user's message/question
            system_prompt: Optional system prompt to guide behavior
            
        Returns:
            The model's response as a string
            
        Note: @abstractmethod means subclasses MUST implement this
        """
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """
        Check if this provider is available/accessible.
        
        Returns:
            True if we can connect, False otherwise
        """
        pass
