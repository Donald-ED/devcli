"""
Ollama Provider

Connects to Ollama running locally on your machine.
Ollama must be installed and running for this to work!

Install Ollama: https://ollama.ai
Start it: ollama serve
Pull models: ollama pull llama3.1
"""
import requests
from typing import Optional
from devcli.providers.base import BaseProvider


class OllamaProvider(BaseProvider):
    """
    Provider for Ollama - runs models locally on your machine.
    
    Ollama exposes a REST API at http://localhost:11434
    We'll make HTTP requests to it to chat with models.
    """
    
    def __init__(self, model_name: str, api_key: Optional[str] = None):
        """
        Initialize Ollama provider.
        
        Args:
            model_name: Model to use (e.g., "llama3.1", "deepseek-r1:7b")
            api_key: Not needed for Ollama (it runs locally)
        """
        super().__init__(model_name, api_key)
        self.base_url = "http://localhost:11434"
        self.api_url = f"{self.base_url}/api/generate"
    
    def is_available(self) -> bool:
        """
        Check if Ollama is running and accessible.

        Returns:
            True if Ollama is running, False otherwise
        """
        try:
            # Try to connect to Ollama
            response = requests.get(self.base_url, timeout=2)
            return response.status_code == 200
        except (requests.ConnectionError, requests.Timeout):
            return False

    @staticmethod
    def list_models() -> list[dict]:
        """
        List all models available in Ollama.

        Returns:
            List of dicts with model info (name, size, modified, etc.)

        Raises:
            ConnectionError: If can't connect to Ollama
        """
        base_url = "http://localhost:11434"
        try:
            response = requests.get(f"{base_url}/api/tags", timeout=5)
            response.raise_for_status()
            data = response.json()
            return data.get('models', [])
        except (requests.ConnectionError, requests.Timeout):
            raise ConnectionError(
                "Cannot connect to Ollama. Make sure it's running!\n"
                "Start with: ollama serve"
            )
        except requests.RequestException as e:
            raise RuntimeError(f"Error listing Ollama models: {e}")

    def chat(self, message: str, system_prompt: Optional[str] = None) -> str:
        """
        Send a message to Ollama and get a response.
        
        Args:
            message: The user's message
            system_prompt: Optional system prompt (e.g., "You are a helpful coding assistant")
            
        Returns:
            The model's response
            
        Raises:
            ConnectionError: If can't connect to Ollama
            RuntimeError: If the API returns an error
        """
        if not self.is_available():
            raise ConnectionError(
                "Cannot connect to Ollama. Make sure it's running!\n"
                "Install: https://ollama.ai\n"
                "Start: ollama serve"
            )
        
        # Build the prompt
        # If there's a system prompt, include it
        full_prompt = message
        if system_prompt:
            full_prompt = f"System: {system_prompt}\n\nUser: {message}"
        
        # Prepare the request
        payload = {
            "model": self.model_name,
            "prompt": full_prompt,
            "stream": False,  # Don't stream - get full response at once
        }
        
        try:
            # Make the request to Ollama
            response = requests.post(
                self.api_url,
                json=payload,
                timeout=120  # Models can take a while to respond
            )
            
            # Check if request was successful
            response.raise_for_status()
            
            # Parse the response
            data = response.json()
            
            # Ollama returns the response in the 'response' field
            if 'response' in data:
                return data['response']
            else:
                raise RuntimeError(f"Unexpected response format: {data}")
                
        except requests.RequestException as e:
            raise RuntimeError(f"Error communicating with Ollama: {e}")
    
    def chat_stream(self, message: str, system_prompt: Optional[str] = None):
        """
        Stream the response token by token (for future use).
        
        This makes responses feel more interactive - you see them
        being generated in real-time like ChatGPT!
        
        Yields:
            Chunks of the response as they arrive
        """
        if not self.is_available():
            raise ConnectionError("Cannot connect to Ollama")
        
        full_prompt = message
        if system_prompt:
            full_prompt = f"System: {system_prompt}\n\nUser: {message}"
        
        payload = {
            "model": self.model_name,
            "prompt": full_prompt,
            "stream": True,  # Enable streaming
        }
        
        try:
            response = requests.post(
                self.api_url,
                json=payload,
                stream=True,
                timeout=120
            )
            response.raise_for_status()
            
            # Yield each chunk as it arrives
            for line in response.iter_lines():
                if line:
                    data = line.decode('utf-8')
                    import json
                    chunk = json.loads(data)
                    if 'response' in chunk:
                        yield chunk['response']
                        
        except requests.RequestException as e:
            raise RuntimeError(f"Error streaming from Ollama: {e}")


# Convenience function to test the provider
if __name__ == "__main__":
    """
    Test the Ollama provider directly.
    
    Run: python src/devcli/providers/ollama.py
    """
    print("Testing Ollama provider...")
    
    provider = OllamaProvider("llama3.1")
    
    if not provider.is_available():
        print("❌ Ollama is not running!")
        print("Start it with: ollama serve")
        exit(1)
    
    print("✓ Ollama is available!")
    print(f"Using model: {provider.model_name}")
    print("\nAsking: What is 2+2?")
    
    try:
        response = provider.chat("What is 2+2? Answer briefly.")
        print(f"\nResponse: {response}")
    except Exception as e:
        print(f"Error: {e}")
