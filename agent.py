"""
Research Assistant Agent using LangGraph.

This agent demonstrates key LangGraph concepts:
- State management with TypedDict
- Graph-based workflow with nodes and edges
- Tool calling and execution
- Conditional routing
- Human-in-the-loop patterns
"""

import operator
from typing import Annotated, Literal, Sequence, TypedDict

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, ToolMessage
from langchain_core.tools import tool
from langchain_ollama import ChatOllama
from langgraph.graph import END, StateGraph
from langgraph.prebuilt import ToolNode

import config
from tools import calculate, get_current_time, search_wikipedia


# Define the agent state
class AgentState(TypedDict):
    """The state of the agent conversation."""

    messages: Annotated[Sequence[BaseMessage], operator.add]
    next_step: str


# Convert our tools to LangChain tools
@tool
def wikipedia_search(query: str) -> str:
    """Search Wikipedia for factual information. ALWAYS use this tool to verify facts about:
    - Numbers, statistics, counts (e.g., number of states, population)
    - Historical dates and events
    - People, places, organizations
    - Any information that requires accuracy
    Use this instead of relying on your internal knowledge to ensure accuracy."""
    return search_wikipedia(query)


@tool
def calculator(expression: str) -> str:
    """Perform mathematical calculations. Provide ONLY a mathematical expression with numbers and operators.
    Examples:
    - "2026 - 1879" (calculate years)
    - "(50 + 26) * 2" (compound calculation)
    - "240 * 0.15" (percentage)
    Do NOT include any text, just the mathematical expression."""
    return calculate(expression)


@tool
def current_time() -> str:
    """Get the current date and time."""
    return get_current_time()


# List of tools available to the agent
tools = [wikipedia_search, calculator, current_time]


def create_agent():
    """Create and configure the research assistant agent."""

    # Initialize the LLM with Ollama
    llm = ChatOllama(
        model=config.get_model_name(),
        base_url=config.get_ollama_url(),
        temperature=0.7,
    )

    # Bind tools to the LLM
    llm_with_tools = llm.bind_tools(tools)

    # Define the agent node
    def call_model(state: AgentState) -> AgentState:
        """Call the LLM to decide on the next action."""
        messages = state["messages"]

        # Add system message on first call to encourage fact-checking
        if len(messages) == 1:
            from langchain_core.messages import SystemMessage

            system_msg = SystemMessage(
                content="""You are a research assistant. When answering questions:
1. ALWAYS use wikipedia_search to verify factual information (numbers, dates, statistics)
2. Use calculator for ONLY mathematical expressions with numbers and operators (e.g., "2026 - 1991")
3. Use current_time for date/time information - get the time FIRST before calculating with it
4. Do not rely on your internal knowledge for facts that can be verified - always search first!
5. Break complex queries into steps: search/get time first, THEN calculate with the results.
6. IMPORTANT: When using calculator, pass ONLY numbers and math operators, never text or function names."""
            )
            messages = [system_msg] + list(messages)

        response = llm_with_tools.invoke(messages)

        # Determine next step based on whether tools are being called
        if hasattr(response, "tool_calls") and response.tool_calls:
            next_step = "tools"
        else:
            next_step = "end"

        return {"messages": [response], "next_step": next_step}

    # Define the routing function
    def should_continue(state: AgentState) -> Literal["tools", "end"]:
        """Determine whether to continue to tools or end."""
        return state["next_step"]

    # Create the graph
    workflow = StateGraph(AgentState)

    # Add nodes
    workflow.add_node("agent", call_model)
    workflow.add_node("tools", ToolNode(tools))

    # Set the entry point
    workflow.set_entry_point("agent")

    # Add conditional edges
    workflow.add_conditional_edges(
        "agent", should_continue, {"tools": "tools", "end": END}
    )

    # Add edge from tools back to agent
    workflow.add_edge("tools", "agent")

    # Compile the graph
    app = workflow.compile()

    return app


def run_agent(query: str, verbose: bool = True):
    """
    Run the agent with a user query.

    Args:
        query: The user's question or request
        verbose: Whether to print intermediate steps

    Returns:
        The final response from the agent
    """
    agent = create_agent()

    # Initial state
    initial_state = {"messages": [HumanMessage(content=query)], "next_step": "agent"}

    if verbose:
        print(f"\n{'=' * 60}")
        print(f"USER: {query}")
        print(f"{'=' * 60}\n")

    # Run the agent
    final_state = None
    for step, state in enumerate(agent.stream(initial_state), 1):
        if verbose:
            print(f"Step {step}:")
            for node_name, node_state in state.items():
                print(f"  Node: {node_name}")
                if "messages" in node_state:
                    for msg in node_state["messages"]:
                        if isinstance(msg, AIMessage):
                            if hasattr(msg, "tool_calls") and msg.tool_calls:
                                print(
                                    f"    🔧 Calling tools: {[tc['name'] for tc in msg.tool_calls]}"
                                )
                            else:
                                print(f"    🤖 AI: {msg.content[:100]}...")
                        elif isinstance(msg, ToolMessage):
                            print(f"    ⚙️  Tool result: {msg.content[:100]}...")
            print()

        final_state = state

    # Extract final response
    if final_state:
        for node_state in final_state.values():
            if "messages" in node_state:
                for msg in reversed(node_state["messages"]):
                    if isinstance(msg, AIMessage) and msg.content:
                        if verbose:
                            print(f"\n{'=' * 60}")
                            print(f"FINAL ANSWER:\n{msg.content}")
                            print(f"{'=' * 60}\n")
                        return msg.content

    return "No response generated"


def interactive_mode():
    """Run the agent in interactive mode."""
    print("\n" + "=" * 60)
    print("Research Assistant Agent (powered by LangGraph + Ollama)")
    print("=" * 60)
    print("Type your questions or 'quit' to exit\n")

    while True:
        try:
            query = input("You: ").strip()

            if not query:
                continue

            if query.lower() in ["quit", "exit", "q"]:
                print("\nGoodbye!")
                break

            run_agent(query, verbose=True)

        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}\n")


if __name__ == "__main__":
    interactive_mode()
