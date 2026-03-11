import requests
from backend.config import OLLAMA_URL, OLLAMA_MODEL


def generate_response(prompt: str) -> str:

    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload)

    data = response.json()

    return data["response"]