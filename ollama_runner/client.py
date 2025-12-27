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
            res = requests.post(url, json=payload, timeout=300)
            res.raise_for_status()
            return res.json()["response"]
        except Exception as e:
            raise OllamaError(str(e))
