"""
Quick test script to verify the agent setup.
"""

import os

# Override config to use llama3:8b which is available
os.environ["OLLAMA_MODEL"] = "llama3:8b"

from agent import run_agent

print("Testing LangGraph Agent with Ollama...")
print("=" * 60)

# Simple test query
query = "What is 2 + 2?"
print(f"\nTest Query: {query}\n")

try:
    response = run_agent(query, verbose=True)
    print("\n✅ Agent test successful!")
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback

    traceback.print_exc()
