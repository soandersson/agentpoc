# Python with LangGraph Dev Container

This dev container provides a complete Python development environment with LangGraph and related libraries pre-configured.

## Included Features

- Python 3.12
- LangGraph and LangChain ecosystem libraries
- Git and common development utilities
- Zsh with Oh My Zsh

## Pre-installed Python Packages

- `langgraph` - Build stateful, multi-actor applications with LLMs
- `langchain` - Core LangChain library
- `langchain-openai` - OpenAI integrations
- `langchain-anthropic` - Anthropic integrations
- `langchain-community` - Community integrations
- `python-dotenv` - Environment variable management

## VS Code Extensions

- Python language support (Pylance)
- Python debugger
- Jupyter notebooks
- Ruff (fast Python linter and formatter)
- TOML and YAML support

## Port Forwarding

The following ports are automatically forwarded:
- 8000 - Common development server port
- 8501 - Streamlit default port

## Getting Started

1. Open this folder in VS Code
2. Click "Reopen in Container" when prompted (or use Command Palette: "Dev Containers: Reopen in Container")
3. Wait for the container to build and dependencies to install
4. Start coding!

## Additional Configuration

To add more Python packages, update the `postCreateCommand` in `.devcontainer/devcontainer.json` or create a `requirements.txt` file in your project root.
