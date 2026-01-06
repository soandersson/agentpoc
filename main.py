"""
Example usage of the Research Assistant Agent.

This script demonstrates various capabilities of the LangGraph agent.
"""

from langchain_core.messages import HumanMessage

from agent import create_agent, run_agent


def example_simple_question():
    """Example: Simple factual question."""
    print("\n" + "=" * 80)
    print("EXAMPLE 1: Simple Wikipedia Search")
    print("=" * 80)

    query = "What is quantum computing?"
    run_agent(query, verbose=True)


def example_calculation():
    """Example: Mathematical calculation."""
    print("\n" + "=" * 80)
    print("EXAMPLE 2: Mathematical Calculation")
    print("=" * 80)

    query = "What is 15% of 240?"
    run_agent(query, verbose=True)


def example_multi_step():
    """Example: Multi-step reasoning with multiple tools."""
    print("\n" + "=" * 80)
    print("EXAMPLE 3: Multi-Step Reasoning")
    print("=" * 80)

    query = "Who was Albert Einstein and what year was he born? Then calculate how old he would be today if he were still alive."
    run_agent(query, verbose=True)


def example_current_info():
    """Example: Getting current information."""
    print("\n" + "=" * 80)
    print("EXAMPLE 4: Current Information")
    print("=" * 80)

    query = "What is the current time?"
    run_agent(query, verbose=True)


def example_complex_query():
    """Example: Complex query requiring multiple tool uses."""
    print("\n" + "=" * 80)
    print("EXAMPLE 5: Complex Multi-Tool Query")
    print("=" * 80)

    query = "Find information about the Python programming language, then calculate how many years it's been since it was first released (it was released in 1991)."
    run_agent(query, verbose=True)


def run_all_examples():
    """Run all example queries."""
    examples = [
        example_simple_question,
        example_calculation,
        example_multi_step,
        example_current_info,
        example_complex_query,
    ]

    for i, example in enumerate(examples, 1):
        try:
            example()
            if i < len(examples):
                input("\nPress Enter to continue to the next example...")
        except Exception as e:
            print(f"\n❌ Error in example: {e}\n")


def custom_query():
    """Run a custom query provided by the user."""
    print("\n" + "=" * 80)
    print("CUSTOM QUERY")
    print("=" * 80)

    query = input("\nEnter your question: ").strip()
    if query:
        run_agent(query, verbose=True)


if __name__ == "__main__":
    print("=" * 80)
    print("Research Assistant Agent - Example Demonstrations")
    print("=" * 80)
    print("\nThis script demonstrates the capabilities of the LangGraph agent.")
    print("\nOptions:")
    print("  1. Run all examples")
    print("  2. Run a custom query")
    print("  3. Enter interactive mode")
    print()

    choice = input("Enter your choice (1-3): ").strip()

    if choice == "1":
        run_all_examples()
    elif choice == "2":
        custom_query()
    elif choice == "3":
        from agent import interactive_mode

        interactive_mode()
    else:
        print("Invalid choice. Running first example...")
        example_simple_question()
