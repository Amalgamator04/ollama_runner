from ollama_runner import OllamaClient

client=OllamaClient()

response=client.generate(
    model="llama3.1:8b",
    prompt="Explain Ollama in one line, answer me in json format with only one key reply and your response must be its value nothing else and it must be in {} to make sure json format"
)

print(response)