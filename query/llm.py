"""Talk to a local Ollama model."""
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "phi3.5"


def ask_ollama(prompt: str) -> str:
    """Sends a prompt to the local Ollama server, returns the full response text."""
    try:
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
    except requests.exceptions.ConnectionError:
        raise RuntimeError(
            "Could not reach Ollama. Is it running? Try: sudo systemctl start ollama"
        )
    except requests.exceptions.Timeout:
        raise RuntimeError("Ollama took too long to respond (>120s). Try a shorter question.")

    return response.json()["response"].strip()


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print('usage: python -m query.answer "<question>" [subject]')
        sys.exit(1)

    question = sys.argv[1]
    subject = sys.argv[2] if len(sys.argv) > 2 else None

    try:
        result = ask(question, subject=subject)
        print(format_answer(result))
    except RuntimeError as e:
        print(f"Error: {e}")
        sys.exit(1)