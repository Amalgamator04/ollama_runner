import requests

def list_models(base_url="http://localhost:11434"):
    res = requests.get(f"{base_url}/api/tags")
    return [m["name"] for m in res.json()["models"]]
