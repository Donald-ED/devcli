#!/usr/bin/env python3
"""
Demo/Test script to simulate what DevCLI looks like with a working Ollama

This creates a fake Ollama server that responds to questions so you can
see how DevCLI works without actually installing Ollama.

Run: python demo.py
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import threading
import time


class FakeOllamaHandler(BaseHTTPRequestHandler):
    """Simulates Ollama API responses"""
    
    # Canned responses for demo purposes
    RESPONSES = {
        "what is python": "Python is a high-level, interpreted programming language known for its simplicity and readability. Created by Guido van Rossum in 1991, it emphasizes code readability with significant whitespace. Python supports multiple programming paradigms and has a vast ecosystem of libraries.",
        
        "what is 2+2": "2 + 2 = 4",
        
        "explain docker": "Docker is a platform for developing, shipping, and running applications in containers. Containers package an application with all its dependencies, making it portable and consistent across different environments. Think of it like a lightweight virtual machine that starts quickly and uses fewer resources.",
        
        "hello": "Hello! I'm a simulated AI assistant. In the real version with Ollama installed, I'd be powered by models like Llama 3.1, DeepSeek R1, or others. How can I help you today?",
        
        "default": "I'm a demo AI assistant simulating what DevCLI would look like with Ollama installed. In reality, I'd be powered by actual LLMs running locally on your machine. The real models can answer questions, write code, explain concepts, and much more!"
    }
    
    def do_GET(self):
        """Handle GET request (health check)"""
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'Ollama is running')
    
    def do_POST(self):
        """Handle POST request (generate response)"""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))
        
        prompt = data.get('prompt', '').lower()
        
        # Find matching response
        response_text = self.RESPONSES['default']
        for key, value in self.RESPONSES.items():
            if key in prompt:
                response_text = value
                break
        
        # Simulate thinking time
        time.sleep(1)
        
        # Send response
        response = {
            'model': data.get('model', 'llama3.1'),
            'response': response_text,
            'done': True
        }
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode('utf-8'))
    
    def log_message(self, format, *args):
        """Suppress logging"""
        pass


def run_fake_ollama():
    """Run the fake Ollama server"""
    server = HTTPServer(('localhost', 11434), FakeOllamaHandler)
    print("🎭 Fake Ollama server running on http://localhost:11434")
    print("📝 This simulates what real Ollama responses would look like")
    print("\nTry these commands in another terminal:")
    print("  devcli ask 'What is Python?'")
    print("  devcli ask 'Explain Docker'")
    print("  devcli ask 'Hello'")
    print("\nPress Ctrl+C to stop\n")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\n👋 Stopping fake Ollama server")
        server.shutdown()


if __name__ == "__main__":
    run_fake_ollama()
