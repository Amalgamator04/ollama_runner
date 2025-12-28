
from ollama_runner import OllamaClient, list_models

print("Available models:", list_models())

client = OllamaClient()

out = client.generate(
    model="smollm2:latest",
    prompt="Explain Ollama in one line, answer me in json format with only one key reply and your response must be its value nothing else and it must be in {} to make sure json format"
)

embeddings = client.get_embeddings(
    model="granite-embedding:30m",
    prompt="This is the text I want to embed"
)

print(out)
print(embeddings)
