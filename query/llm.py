"""Talk to a local Ollama model."""
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "phi3.5"


def ask_ollama(prompt: str) -> str:
    """Sends a prompt to the local Ollama server, returns the full response text."""
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {"num_predict": 512},
        },
        timeout=120,
    )
    response.raise_for_status()
    return response.json()["response"].strip()


if __name__ == "__main__":
    import sys
    prompt = sys.argv[1] if len(sys.argv) > 1 else "Say hello in one sentence."
    print(ask_ollama(prompt))