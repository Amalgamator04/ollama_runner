import requests
from typing import List, Callable

def list_models(base_url="http://localhost:11434"):
    res = requests.get(f"{base_url}/api/tags")
    return [m["name"] for m in res.json()["models"]]

def list_function_names(tools: List[Callable]) -> List[str]:
    """
    List the names of functions in a list of callable tools.
    
    Args:
        tools: A list of callable functions/tools
        
    Returns:
        A list of function names
    """
    return [func.__name__ for func in tools]
