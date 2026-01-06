"""
Setup helper script to verify Ollama connection and models.
"""

import json
import sys

import requests


def check_ollama_connection(base_url="http://host.docker.internal:11434"):
    """Check if Ollama is accessible."""
    try:
        response = requests.get(f"{base_url}/api/tags", timeout=5)
        if response.status_code == 200:
            return True, response.json()
        return False, f"Unexpected status code: {response.status_code}"
    except requests.exceptions.ConnectionError:
        return False, "Connection refused. Is Ollama running on your host?"
    except Exception as e:
        return False, str(e)


def check_model_tool_support(model_name):
    """
    Check if a model supports tool calling.
    Models with tool support: llama3.2, llama3.1, qwen2.5, mistral, phi3.5
    """
    tool_supporting_models = [
        "llama3.2",
        "llama3.1",
        "llama3.3",
        "qwen2.5",
        "qwen2",
        "mistral",
        "mixtral",
        "phi3.5",
        "phi4",
        "command-r",
    ]

    model_base = model_name.split(":")[0].lower()
    return any(supported in model_base for supported in tool_supporting_models)


def main():
    print("=" * 70)
    print("LangGraph Agent - Setup Verification")
    print("=" * 70)

    # Check connection
    print("\n1. Checking Ollama connection...")
    success, result = check_ollama_connection()

    if not success:
        print(f"   ❌ Failed to connect: {result}")
        print("\nTroubleshooting:")
        print("  - Ensure Ollama is running on your host machine")
        print("  - Try: export OLLAMA_BASE_URL=http://172.17.0.1:11434")
        print("  - Or configure devcontainer to use --network=host")
        sys.exit(1)

    print("   ✅ Successfully connected to Ollama")

    # List models
    models = result.get("models", [])
    print(f"\n2. Available models ({len(models)}):")

    if not models:
        print("   ❌ No models found!")
        print("\nOn your host machine, pull a model:")
        print("  ollama pull llama3.2")
        sys.exit(1)

    tool_models = []
    non_tool_models = []

    for model in models:
        model_name = model["name"]
        supports_tools = check_model_tool_support(model_name)
        size_gb = model["size"] / (1024**3)

        if supports_tools:
            tool_models.append((model_name, size_gb))
            print(f"   ✅ {model_name} ({size_gb:.1f}GB) - Supports tool calling")
        else:
            non_tool_models.append((model_name, size_gb))
            print(f"   ⚠️  {model_name} ({size_gb:.1f}GB) - No tool calling support")

    # Recommendations
    print("\n3. Recommendations:")

    if tool_models:
        print(
            f"   ✅ Great! You have {len(tool_models)} model(s) with tool calling support"
        )
        print(f"\n   To use: export OLLAMA_MODEL={tool_models[0][0]}")
        print(f"   Or in .env file: OLLAMA_MODEL={tool_models[0][0]}")
    else:
        print("   ⚠️  No models with native tool calling support found")
        print("\n   Recommended: Pull a model with tool support:")
        print("   On your host machine, run:")
        print("     ollama pull llama3.2     # Fast, 2GB, supports tools")
        print("     ollama pull qwen2.5:3b   # Alternative, 2GB")
        print("     ollama pull llama3.1     # More capable, larger")

        if non_tool_models:
            print(
                f"\n   You can still use {non_tool_models[0][0]}, but with limited functionality"
            )

    print("\n4. Next steps:")
    print("   - Run: python test_agent.py")
    print("   - Or: python agent.py (interactive mode)")
    print("   - Or: python main.py (examples)")

    print("\n" + "=" * 70)
    print("Setup verification complete!")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
