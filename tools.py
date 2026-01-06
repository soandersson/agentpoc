"""
Tools for the research assistant agent.
These tools provide capabilities for searching information and performing calculations.
"""

import json
from datetime import datetime
from typing import Optional

import wikipedia


def search_wikipedia(query: str) -> str:
    """
    Search Wikipedia for information on a topic.

    Args:
        query: The search query

    Returns:
        A summary of the Wikipedia article, or an error message
    """
    try:
        # Search for the page
        search_results = wikipedia.search(query, results=3)
        if not search_results:
            return f"No Wikipedia results found for '{query}'"

        # Get the first result's summary
        page = wikipedia.page(search_results[0], auto_suggest=False)
        summary = wikipedia.summary(search_results[0], sentences=5, auto_suggest=False)

        return f"**{page.title}**\n\n{summary}\n\nSource: {page.url}"

    except wikipedia.exceptions.DisambiguationError as e:
        # Multiple results - return options
        options = ", ".join(e.options[:5])
        return f"Multiple results found. Please be more specific. Options: {options}"

    except wikipedia.exceptions.PageError:
        return f"No Wikipedia page found for '{query}'"

    except Exception as e:
        return f"Error searching Wikipedia: {str(e)}"


def calculate(expression: str) -> str:
    """
    Safely evaluate a mathematical expression.

    Args:
        expression: A mathematical expression (e.g., "2 + 2 * 3")

    Returns:
        The result of the calculation or an error message
    """
    try:
        # Clean up the expression
        expression = expression.strip()

        # Replace common problematic characters
        expression = expression.replace("−", "-")  # Unicode minus
        expression = expression.replace("–", "-")  # En-dash
        expression = expression.replace("—", "-")  # Em-dash
        expression = expression.replace("×", "*")  # Multiplication sign
        expression = expression.replace("÷", "/")  # Division sign
        expression = expression.replace(",", "")  # Remove commas from numbers

        # Basic safety - only allow math operations
        allowed_chars = set("0123456789+-*/.()**% ")
        if not all(c in allowed_chars for c in expression):
            invalid_chars = set(c for c in expression if c not in allowed_chars)
            return f"Error: Expression contains invalid characters: {invalid_chars}. Only numbers and basic math operators (+, -, *, /, **, %, parentheses) are allowed. Your expression: '{expression}'"

        # Evaluate the expression
        result = eval(expression, {"__builtins__": {}}, {})
        return f"Result: {result}"

    except Exception as e:
        return f"Error calculating '{expression}': {str(e)}"


def get_current_time() -> str:
    """
    Get the current date and time.

    Returns:
        The current date and time as a formatted string
    """
    now = datetime.now()
    return f"Current date and time: {now.strftime('%Y-%m-%d %H:%M:%S %Z')}"


# Tool definitions for the agent
TOOL_DEFINITIONS = [
    {
        "name": "search_wikipedia",
        "description": "Search Wikipedia for information about a topic. Use this when you need factual information about people, places, events, concepts, or any general knowledge.",
        "function": search_wikipedia,
    },
    {
        "name": "calculate",
        "description": "Perform mathematical calculations. Use this for any arithmetic operations, algebraic expressions, or numerical computations.",
        "function": calculate,
    },
    {
        "name": "get_current_time",
        "description": "Get the current date and time. Use this when you need to know what time it is or what the current date is.",
        "function": get_current_time,
    },
]


def get_tools():
    """Return the list of available tools."""
    return TOOL_DEFINITIONS
