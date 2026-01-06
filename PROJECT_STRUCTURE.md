# Project Structure

```
agentpoc/
├── README.md                 # Main documentation
├── LEARNING_GUIDE.md        # In-depth learning guide
├── requirements.txt         # Python dependencies
├── .env.example            # Environment configuration template
├── .gitignore              # Git ignore rules
│
├── config.py               # Configuration (Ollama URL, model selection)
├── tools.py                # Tool implementations (Wikipedia, calculator, etc.)
├── agent.py                # Main LangGraph agent implementation
│
├── main.py                 # Example usage and demonstrations
├── test_agent.py           # Quick test script
├── setup_check.py          # Setup verification tool
└── visualize_graph.py      # Graph structure visualization
```

## 📁 File Descriptions

### Core Files

**agent.py** - The heart of the project
- Defines the agent state (`AgentState`)
- Creates LangGraph nodes and edges
- Implements the ReAct loop
- Provides `run_agent()` and `interactive_mode()` functions

**tools.py** - Tool implementations
- `search_wikipedia()`: Search Wikipedia articles
- `calculate()`: Safe math evaluation
- `get_current_time()`: Get current date/time
- Tool definitions for LangGraph

**config.py** - Configuration management
- Ollama connection settings
- Model selection
- Feature flags

### Utility Files

**setup_check.py** - Verify your setup
- Tests Ollama connection
- Lists available models
- Checks tool calling support
- Provides recommendations

**visualize_graph.py** - Understand the workflow
- Generates Mermaid diagram of the agent graph
- Shows the flow of data through nodes
- Helps visualize the architecture

**main.py** - Learn by example
- Pre-built example queries
- Demonstrates different capabilities
- Shows multi-step reasoning

**test_agent.py** - Quick smoke test
- Simple test to verify everything works
- Good for debugging connection issues

### Documentation

**README.md** - Start here
- Quick start guide
- Setup instructions
- Usage examples
- Troubleshooting

**LEARNING_GUIDE.md** - Deep dive
- Concept explanations
- Extension ideas
- Learning exercises
- Best practices

## 🚀 Quick Commands

```bash
# Verify setup
python setup_check.py

# Interactive mode
python agent.py

# Run examples
python main.py

# Quick test
python test_agent.py

# Visualize graph
python visualize_graph.py
```

## 🔑 Key Concepts by File

### State Management → agent.py
```python
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    next_step: str
```

### Graph Construction → agent.py
```python
workflow = StateGraph(AgentState)
workflow.add_node("agent", call_model)
workflow.add_node("tools", ToolNode(tools))
workflow.add_conditional_edges("agent", should_continue, {...})
```

### Tool Definition → tools.py
```python
def search_wikipedia(query: str) -> str:
    """Search Wikipedia for information."""
    # Implementation
```

### Tool Integration → agent.py
```python
@tool
def wikipedia_search(query: str) -> str:
    return search_wikipedia(query)

tools = [wikipedia_search, calculator, current_time]
llm_with_tools = llm.bind_tools(tools)
```

## 🎯 Learning Path

1. **Run setup_check.py** - Ensure everything is configured
2. **Read README.md** - Understand what the project does
3. **Run main.py** - See examples in action
4. **Read agent.py** - Understand the implementation
5. **Read LEARNING_GUIDE.md** - Learn concepts deeply
6. **Run visualize_graph.py** - Visualize the workflow
7. **Modify tools.py** - Add your own tools
8. **Extend agent.py** - Build more complex workflows

## 💡 Common Tasks

### Change the Model
```python
# Option 1: Environment variable
export OLLAMA_MODEL=llama3.2

# Option 2: Edit config.py
DEFAULT_MODEL = "llama3.2"

# Option 3: .env file
OLLAMA_MODEL=llama3.2
```

### Add a New Tool
1. Implement function in `tools.py`
2. Add `@tool` decorator in `agent.py`
3. Add to `tools` list in `agent.py`

### Debug Issues
1. Run `setup_check.py` for diagnostics
2. Check Ollama connection: `curl http://host.docker.internal:11434/api/tags`
3. Enable verbose mode: `run_agent(query, verbose=True)`

### Extend Functionality
- See `LEARNING_GUIDE.md` for extension patterns
- Study the examples in `main.py`
- Experiment with different graph structures

## 📚 Additional Resources

- Agent code: [agent.py](agent.py)
- Tool examples: [tools.py](tools.py)
- Configuration: [config.py](config.py)
- Learning guide: [LEARNING_GUIDE.md](LEARNING_GUIDE.md)
- Main docs: [README.md](README.md)
