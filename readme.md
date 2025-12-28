# Ollama Runner

A lightweight Python client for running local Ollama models. This library provides a simple and intuitive interface to interact with Ollama's API, making it easy to generate text using locally hosted large language models.

## Why Ollama Runner?

Ollama Runner simplifies the process of interacting with Ollama models in Python. Instead of manually crafting HTTP requests, you can use this library to:

- **Easy Integration**: Simple Python API for interacting with Ollama models
- **Lightweight**: Minimal dependencies (only requires `requests`)
- **Local AI**: Run powerful language models on your local machine with privacy
- **No Cloud Costs**: Use free, open-source models without API costs
- **Fast Development**: Quick setup and straightforward API for rapid prototyping

## Prerequisites

Before installing `ollama-runner`, you need to have Ollama installed and running on your system.

### Installing Ollama

1. **Download Ollama**: Visit [https://ollama.com](https://ollama.com) and download Ollama for your operating system (Windows, macOS, or Linux).

2. **Install Ollama**: Follow the installation instructions for your platform.

3. **Run Ollama Server**: For the first time, you need to start the Ollama server:
   ```bash
   ollama serve
   ```
   This will start the Ollama server on `http://localhost:11434` (default port).

4. **Pull a Model** (Optional but recommended): Download a model to use:
   ```bash
   ollama pull llama3.1:8b
   ```
   You can choose from various models like `llama3.1:8b`, `mistral`, `codellama`, etc.

**Note**: The `ollama serve` command needs to be running in a separate terminal/process while you use this library. Keep that terminal open while working with ollama-runner.

## Installation

Install `ollama-runner` directly from GitHub using pip:

```bash
pip install git+https://github.com/Amalgamator04/ollama_runner.git
```

This library is currently only available on GitHub and not published on PyPI, so you must install it using the GitHub repository URL.

## Usage Examples

### Basic Usage

```python
from ollama_runner import OllamaClient, list_models

# List available models
print("Available models:", list_models())

# Create a client (defaults to http://localhost:11434)
client = OllamaClient()

# Generate text
response = client.generate(
    model="llama3.1:8b",
    prompt="Explain what Python is in one sentence."
)

print(response)
```

### Custom Ollama Server

If your Ollama server is running on a different host or port:

```python
from ollama_runner import OllamaClient

# Connect to a custom Ollama server
client = OllamaClient(base_url="http://localhost:11434")

response = client.generate(
    model="mistral",
    prompt="Write a haiku about coding."
)

print(response)
```

### Complete Example

```python
from ollama_runner import OllamaClient, list_models

# Check what models are available
available_models = list_models()
print(f"Available models: {available_models}")

# Initialize the client
client = OllamaClient()

# Generate a response
result = client.generate(
    model="llama3.1:8b",
    prompt="What are the benefits of using local AI models?"
)

print("Generated response:")
print(result)
```

### Getting Embeddings

Generate embeddings for text using embedding models (useful for semantic search, similarity matching, etc.):

```python
from ollama_runner import OllamaClient

client = OllamaClient()

# Get embeddings for text
embeddings = client.get_embeddings(
    model="granite-embedding:30m",
    prompt="This is the text I want to embed"
)

print(f"Embedding vector (length: {len(embeddings)}):")
print(embeddings[:10])  # Print first 10 dimensions
```

**Note**: Make sure you have an embedding model installed. You can pull one using:
```bash
ollama pull granite-embedding:30m
```

## API Reference

### `OllamaClient`

The main client class for interacting with Ollama.

#### `__init__(base_url: str = "http://localhost:11434")`

Initialize the Ollama client.

- `base_url`: The base URL of your Ollama server (default: `http://localhost:11434`)

#### `generate(model: str, prompt: str) -> str`

Generate text using the specified model.

- `model`: The name of the model to use (e.g., `"llama3.1:8b"`, `"mistral"`)
- `prompt`: The input prompt for text generation
- Returns: The generated text response as a string
- Raises: `OllamaError` if the request fails

#### `get_embeddings(model: str, prompt: str) -> list`

Get embeddings for the input text using an embedding model.

- `model`: The name of the embedding model to use (e.g., `"granite-embedding:30m"`)
- `prompt`: The input text to generate embeddings for
- Returns: A list of floats representing the embedding vector
- Raises: `OllamaError` if the request fails

**Note**: Embedding models require input text. Make sure to provide text in the `prompt` parameter.

### `list_models(base_url: str = "http://localhost:11434") -> list`

List all available models on the Ollama server.

- `base_url`: The base URL of your Ollama server (default: `http://localhost:11434`)
- Returns: A list of model names

## Requirements

- Python 3.9 or higher
- `requests` library (automatically installed with ollama-runner)
- Ollama installed and running on your system

## Error Handling

The library raises `OllamaError` when requests fail. Make sure:

1. Ollama server is running (`ollama serve`)
2. The specified model is available (use `list_models()` to check)
3. The base URL is correct
4. Your network connection is working

```python
from ollama_runner import OllamaClient, OllamaError

client = OllamaClient()

try:
    response = client.generate(model="llama3.1:8b", prompt="Hello!")
    print(response)
except OllamaError as e:
    print(f"Error: {e}")
```

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

