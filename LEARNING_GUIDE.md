# LangGraph Learning Guide

This document explains the key concepts demonstrated in this project and how to extend it for your own learning.

## 🎓 Core Concepts Explained

### 1. State Management

**What it is**: State represents the information that flows through your agent as it processes a task.

**In this project**: We use `AgentState` (a TypedDict) to track:
- **messages**: The conversation history (user inputs, AI responses, tool calls)
- **next_step**: Where the agent should go next in the graph

```python
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    next_step: str
```

**Key insight**: The `Annotated[..., operator.add]` means messages get appended rather than replaced.

### 2. Graph Construction

**What it is**: A graph defines the workflow of your agent - nodes represent actions, edges represent transitions.

**In this project**: We have a simple but powerful graph:
```
[User Input] → [Agent Node] → [Tools Node] → [Agent Node] → ... → [End]
                     ↓
                   [End]
```

**Nodes**:
- **agent**: Decides whether to call tools or respond
- **tools**: Executes the selected tools
- **END**: Terminal node (conversation ends)

**Edges**:
- **Conditional edge** from agent: Goes to tools if tool calls are needed, otherwise ends
- **Regular edge** from tools: Always returns to agent

### 3. Tool Integration

**What it is**: Tools give your LLM the ability to interact with external systems or perform specific actions.

**In this project**: We have three tools:
1. `wikipedia_search`: Retrieves factual information
2. `calculator`: Performs math operations
3. `current_time`: Gets date/time

**How it works**:
1. LLM receives user query
2. LLM decides which tool(s) to call (if any)
3. Tools execute and return results
4. LLM uses results to formulate response

### 3.1 Controlling Tool Selection with Descriptions

**Important Learning**: Tool descriptions directly influence when the LLM chooses to use them.

**Example - Basic description (less effective)**:
```python
@tool
def wikipedia_search(query: str) -> str:
    """Search Wikipedia for information on a topic."""
    return search_wikipedia(query)
```
Problem: LLM may use internal knowledge instead of searching.

**Example - Enhanced description (more effective)**:
```python
@tool
def wikipedia_search(query: str) -> str:
    """Search Wikipedia for factual information. ALWAYS use this tool to verify facts about:
    - Numbers, statistics, counts (e.g., number of states, population)
    - Historical dates and events
    - People, places, organizations
    - Any information that requires accuracy
    Use this instead of relying on your internal knowledge to ensure accuracy."""
    return search_wikipedia(query)
```

**Result**: The detailed description with explicit use cases guides the LLM to prioritize tool usage.

### 3.2 System Prompts for Behavior Control

**What it is**: A system message that sets behavioral guidelines for the agent.

**In this project**: We inject a system prompt on the first call:
```python
def call_model(state: AgentState) -> AgentState:
    messages = state["messages"]
    
    # Add system message on first call
    if len(messages) == 1:
        system_msg = SystemMessage(content="""You are a research assistant. When answering questions:
1. ALWAYS use wikipedia_search to verify factual information (numbers, dates, statistics)
2. Use calculator for any mathematical operations
3. Use current_time for date/time information
4. Do not rely on your internal knowledge for facts that can be verified - always search first!
5. Break complex queries into steps: search for facts first, then calculate.""")
        messages = [system_msg] + list(messages)
    
    response = llm_with_tools.invoke(messages)
```

**Why this matters**:
- Without system prompt: LLM uses internal knowledge (may be outdated/incorrect)
- With system prompt: LLM searches Wikipedia first (verifiable, current information)

**Test case**:
- Query: "Number of US states + Brazil states, then multiply"
- Without prompt: Uses internal knowledge (50 + 26)
- With prompt: Calls Wikipedia twice, then calculates

### 3.3 Common Tool Calling Issues

**Issue #1: Invalid Calculator Input**

**Symptom**: Error like `Expression contains invalid characters: {'"', 'c', 'n', 'r', '_', 't', 'e'}`

**Cause**: The LLM passes text or function names instead of numbers to the calculator.

**Example of what went wrong**:
```python
# What the LLM might have tried to do:
calculator("current_time - 1991")  # ❌ Wrong - contains text
calculator("2026 - 1991")          # ✅ Correct - only numbers
```

**Why it happens**: When calling multiple tools simultaneously, the LLM might:
1. Mix up which argument goes to which tool
2. Try to use one tool's output as another tool's input (before getting results)
3. Include text/variable names in mathematical expressions

**Solutions**:
1. **Better tool descriptions** - Explicitly state what format is expected
2. **Input validation** - Clean and validate inputs (like our improved calculator)
3. **Sequential execution** - Use system prompt to encourage step-by-step: search first, then calculate
4. **Error recovery** - When a tool fails, the agent can try again with corrected input

**Real example from this project**:
```
Query: "Calculate years since Python was released in 1991"

❌ Bad approach (parallel):
  - Calls wikipedia_search AND calculator simultaneously
  - Calculator gets "current_time - 1991" (text!)
  - Error occurs

✅ Good approach (sequential):
  - Call current_time first → get "2026"
  - Then call calculator("2026 - 1991") → get "35"
  - Return answer
```

**The fix**: Our improved calculator now:
- Strips whitespace and cleans input
- Provides clear error messages showing what was invalid
- Handles unicode characters and common formatting issues

### 4. ReAct Pattern

**What it is**: Reasoning and Acting - the LLM alternates between reasoning about what to do and taking actions.

**In this project**: You can see this in the output:
```
Step 1: [Agent decides to call wikipedia_search]
Step 2: [Tool executes and returns data]
Step 3: [Agent reasons about the data]
Step 4: [Agent provides final answer]
```

### 5. Conditional Routing

**What it is**: The graph flow changes based on the current state.

**In this project**: The `should_continue` function checks if the LLM called any tools:
- If yes → go to tools node
- If no → end the conversation

## 🔧 How to Extend This Project

### Adding New Tools

1. **Create the tool function** in [tools.py](tools.py):
```python
def my_new_tool(param: str) -> str:
    """Tool description for the LLM."""
    # Your implementation
    return "result"
```

2. **Decorate it as a tool** in [agent.py](agent.py):
```python
@tool
def my_new_tool_wrapper(param: str) -> str:
    """Tool description."""
    return my_new_tool(param)

# Add to tools list
tools = [wikipedia_search, calculator, current_time, my_new_tool_wrapper]
```

**Ideas for new tools**:
- Weather lookup
- Code execution
- File operations
- API calls
- Database queries

### Adding Memory/History

**Challenge**: Make the agent remember previous conversations.

**Solution**: Extend the state to include conversation history:
```python
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    conversation_id: str
    user_preferences: dict
    next_step: str
```

### Adding Human-in-the-Loop

**Challenge**: Get user approval before executing certain actions.

**Solution**: Add an interrupt before sensitive operations:
```python
# In your graph
workflow.add_node("ask_human", ask_human_node)

def should_ask_human(state):
    # Check if action needs approval
    if needs_approval:
        return "ask_human"
    return "continue"
```

### Multi-Agent Systems

**Challenge**: Create multiple specialized agents that work together.

**Solution**: Create separate graphs for each agent and coordinate:
```python
# Research agent
research_agent = create_research_agent()

# Analysis agent  
analysis_agent = create_analysis_agent()

# Coordinator
def coordinator(query):
    research_result = research_agent.invoke(query)
    analysis = analysis_agent.invoke(research_result)
    return analysis
```

## 📚 LangGraph Patterns to Learn

### 1. Map-Reduce Pattern
Process items in parallel then combine results:
```
[Input] → [Map: Process each item] → [Reduce: Combine] → [Output]
```

### 2. Router Pattern
Direct queries to specialized sub-agents:
```
[Query] → [Router] → [Specialist A]
                  → [Specialist B]
                  → [Specialist C]
```

### 3. Plan-and-Execute Pattern
Create a plan, then execute steps:
```
[Query] → [Planner] → [Executor] → [Verifier] → [Output]
                          ↑             ↓
                          └─────[Loop]──┘
```

### 4. Reflection Pattern
Agent reviews and improves its own outputs:
```
[Generate] → [Reflect] → [Revise] → [Reflect] → ... → [Final]
```

## 🧪 Learning Exercises

### Exercise 1: Add a Weather Tool
Create a tool that fetches weather information (you can use a mock or real API).

### Exercise 2: Implement Conversation History
Modify the agent to remember the last 5 interactions and use them for context.

### Exercise 3: Add a Planning Step
Before answering, have the agent create a plan of steps it will take.

### Exercise 4: Create a Specialized Agent
Build a coding assistant that can search documentation and explain code.

### Exercise 5: Build Multi-Turn Reasoning
Implement a graph where the agent can ask follow-up questions before answering.

## 🐛 Common Patterns for Debugging

### 1. Print State at Each Node
```python
def my_node(state):
    print(f"State at my_node: {state}")
    # Process
    return updated_state
```

### 2. Visualize the Graph
```python
from langchain_core.runnables.graph import CurveStyle, MermaidDrawMethod

agent = create_agent()
print(agent.get_graph().draw_mermaid())
```

### 3. Step Through Execution
Use the verbose flag and watch each step:
```python
for step, state in enumerate(agent.stream(initial_state)):
    print(f"Step {step}: {state}")
    input("Press Enter for next step...")
```

## 📖 Recommended Resources

### Documentation
- [LangGraph Docs](https://langchain-ai.github.io/langgraph/)
- [LangGraph Tutorials](https://langchain-ai.github.io/langgraph/tutorials/)
- [LangChain Docs](https://python.langchain.com/)

### Example Projects
- LangGraph Examples Repository
- Anthropic Claude Examples
- OpenAI Function Calling Examples

### Concepts to Study
- Finite State Machines
- Graph Theory basics
- ReAct prompting
- Chain of Thought reasoning
- Tool use in LLMs

## 🎯 Next Steps

1. **Understand the basics**: Run the examples and study the code
2. **Modify existing tools**: Change how tools work
3. **Add new tools**: Implement your own tools
4. **Redesign the graph**: Create more complex workflows
5. **Build a project**: Apply what you learned to a real problem

## 💡 Project Ideas

1. **Customer Support Bot**: Route queries, search knowledge base, escalate to humans
2. **Research Assistant**: Search multiple sources, synthesize information, cite sources
3. **Code Review Agent**: Analyze code, suggest improvements, check standards
4. **Data Analysis Agent**: Load data, analyze patterns, generate visualizations
5. **Content Generator**: Research topics, create outlines, write drafts, revise

Happy learning! 🚀
