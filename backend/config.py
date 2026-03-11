"""
Central configuration for the stakeholder simulation system.
"""

# LLM Provider

LLM_PROVIDER = "ollama"


# Ollama Configuration

OLLAMA_URL = "http://localhost:11434/api/generate"

OLLAMA_MODEL = "llama3.1"

# generation Settings

LLM_TEMPERATURE = 0.3

MAX_RESPONSE_TOKENS = 800

# simulation Settings

MAX_CHUNKS_PER_RESPONSE = 5

MAX_MEETING_TURNS = 25