import requests
from .exceptions import OllamaError

OLLAMA_BASE_URL = "http://localhost:11434"

class OllamaClient:
    def __init__(self, base_url: str = OLLAMA_BASE_URL):
        self.base_url = base_url.rstrip("/")

    def generate(self, model: str, prompt: str) -> str:
        url = f"{self.base_url}/api/generate"

        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False
        }

        try:
            res = requests.post(url, json=payload, timeout=1000)
            res.raise_for_status()
            return res.json()["response"]
        except Exception as e:
            raise OllamaError(str(e))

    def get_embeddings(self, model: str, prompt: str) -> list:
        """
        Get embeddings for the input text using the specified embedding model.
        
        Args:
            model: The name of the embedding model to use (e.g., "granite-embedding:30m")
            prompt: The input text to generate embeddings for
            
        Returns:
            A list of floats representing the embedding vector
        """
        url = f"{self.base_url}/api/embeddings"

        payload = {
            "model": model,
            "prompt": prompt
        }

        try:
            res = requests.post(url, json=payload, timeout=300)
            res.raise_for_status()
            return res.json()["embedding"]
        except Exception as e:
            raise OllamaError(str(e))