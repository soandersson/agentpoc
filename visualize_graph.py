"""
Visualize the agent's graph structure.
This script generates a visual representation of the LangGraph workflow.
"""

from agent import create_agent


def visualize_graph():
    """Generate and print the Mermaid diagram of the agent graph."""
    print("=" * 70)
    print("LangGraph Agent Architecture Visualization")
    print("=" * 70)
    print("\nGenerating graph visualization...\n")

    try:
        agent = create_agent()
        mermaid_code = agent.get_graph().draw_mermaid()

        print("Mermaid Diagram:")
        print("-" * 70)
        print(mermaid_code)
        print("-" * 70)

        print("\n" + "=" * 70)
        print("Graph Components:")
        print("=" * 70)
        print("\n1. START → agent")
        print("   Entry point: User query comes in")

        print("\n2. agent → tools OR agent → END")
        print("   Decision: Does the agent need to use tools?")
        print("   - YES: Go to tools node")
        print("   - NO: End and return response")

        print("\n3. tools → agent")
        print("   Execution: Tools run and return results to agent")

        print("\n4. Loop: agent ⟷ tools")
        print("   Iteration: Agent can call tools multiple times")

        print("\n" + "=" * 70)
        print("To visualize this graph:")
        print("=" * 70)
        print("1. Copy the Mermaid code above")
        print("2. Visit: https://mermaid.live/")
        print("3. Paste the code to see the visual diagram")
        print("=" * 70 + "\n")

    except Exception as e:
        print(f"Error generating visualization: {e}")
        print("\nManual graph structure:")
        print("""
        ┌──────────┐
        │  START   │
        └────┬─────┘
             │
             ▼
        ┌────────────┐
        │   agent    │ (Decides: call tools or end?)
        └────┬───┬───┘
             │   │
    ┌────────┘   └────────┐
    │                     │
    ▼                     ▼
┌────────┐           ┌────────┐
│ tools  │           │  END   │
└───┬────┘           └────────┘
    │
    └──────────────────┐
                       │
                       ▼
                 (back to agent)
        """)


if __name__ == "__main__":
    visualize_graph()
