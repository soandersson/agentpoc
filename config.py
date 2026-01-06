"""
Configuration for the LangGraph agent.
This connects to Ollama running on the host machine from the dev container.
"""

import os
from typing import Optional

# Ollama configuration
# From within a dev container, the host machine is typically accessible via:
# - host.docker.internal (Windows/Mac)
# - 172.17.0.1 (Linux default docker bridge)
# You can also pass through the host network with --network=host
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://host.docker.internal:11434")

# Model configuration
# For full tool-calling support, use: llama3.2, llama3.1, qwen2.5, mistral, phi3.5
# Fallback mode (without native tools) works with: llama3, llama2, etc.
DEFAULT_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")
USE_TOOL_CALLING = os.getenv("USE_TOOL_CALLING", "true").lower() == "true"

# Agent configuration
MAX_ITERATIONS = 10
RECURSION_LIMIT = 25

# Tool configuration
ENABLE_WEB_SEARCH = os.getenv("ENABLE_WEB_SEARCH", "false").lower() == "true"
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "")  # Optional: for web search


def get_ollama_url() -> str:
    """Get the Ollama base URL for the current environment."""
    return OLLAMA_BASE_URL


def get_model_name() -> str:
    """Get the configured model name."""
    return DEFAULT_MODEL
