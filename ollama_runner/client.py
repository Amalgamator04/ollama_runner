import requests
import inspect
from typing import List, Callable, Dict, Any, get_origin
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

    def _function_to_tool_schema(self, func: Callable) -> Dict[str, Any]:
        """
        Convert a Python function to Ollama tool schema format.
        
        Args:
            func: The Python function to convert
            
        Returns:
            A dictionary representing the tool schema
        """
        sig = inspect.signature(func)
        docstring = inspect.getdoc(func) or ""
        
        # Extract parameters
        properties = {}
        required = []
        
        for param_name, param in sig.parameters.items():
            param_type = "string"  # default
            if param.annotation != inspect.Parameter.empty:
                # Check for built-in types
                if param.annotation == str:
                    param_type = "string"
                elif param.annotation == int:
                    param_type = "integer"
                elif param.annotation == float:
                    param_type = "number"
                elif param.annotation == bool:
                    param_type = "boolean"
                elif param.annotation == list:
                    param_type = "array"
                elif param.annotation == dict:
                    param_type = "object"
                else:
                    # Handle generic types like list[float], List[str], etc.
                    origin = get_origin(param.annotation)
                    if origin is not None:
                        if origin == list:
                            param_type = "array"
                        elif origin == dict:
                            param_type = "object"
                    else:
                        param_type = "string"
            
            properties[param_name] = {
                "type": param_type,
                "description": param_name
            }
            
            if param.default == inspect.Parameter.empty:
                required.append(param_name)
        
        return {
            "type": "function",
            "function": {
                "name": func.__name__,
                "description": docstring.split('\n')[0] if docstring else f"Function {func.__name__}",
                "parameters": {
                    "type": "object",
                    "properties": properties,
                    "required": required
                }
            }
        }

    def decide_tool(self, model: str, messages: List[Dict[str, str]], tools: List[Callable]) -> Dict[str, Any]:
        """
        Use Ollama to decide which tool to use based on the conversation messages.
        
        Args:
            model: The name of the model to use (e.g., "functiongemma")
            messages: A list of message dictionaries with "role" and "content" keys
            tools: A list of Python functions that will be converted to tool schemas
            
        Returns:
            A dictionary containing the response from Ollama, including tool calls if any
        """
        url = f"{self.base_url}/api/chat"
        
        # Convert Python functions to tool schemas
        tool_schemas = [self._function_to_tool_schema(tool) for tool in tools]
        
        payload = {
            "model": model,
            "messages": messages,
            "tools": tool_schemas,
            "stream": False
        }
        
        try:
            res = requests.post(url, json=payload, timeout=1000)
            res.raise_for_status()
            return res.json()
        except Exception as e:
            raise OllamaError(str(e))