# LangGraph Research Assistant Agent

A learning-focused implementation of an AI agent using **LangGraph** and **Ollama**, demonstrating key concepts like state management, tool calling, conditional routing, and graph-based workflows.

## 🚀 Quick Start

```bash
# 1. Verify setup (checks Ollama connection and models)
python setup_check.py

# 2. If needed, pull a compatible model on your HOST machine:
ollama pull llama3.2

# 3. Run the agent
python agent.py              # Interactive mode
# OR
python main.py               # Example demonstrations
```

## 🎯 Project Overview

This project implements a **Research Assistant Agent** that can:
- 🔍 Search Wikipedia for factual information
- 🧮 Perform mathematical calculations
- ⏰ Get current date and time information
- 🤔 Reason through multi-step problems
- 🔄 Orchestrate multiple tools to answer complex queries

## 🏗️ Architecture

The agent is built using **LangGraph**, which provides a graph-based framework for building stateful, multi-actor applications with LLMs.

### Key Components:

```
┌─────────────┐
│   User      │
│   Query     │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────┐
│         LangGraph Agent             │
│  ┌───────────────────────────────┐  │
│  │     State Management          │  │
│  │  (Messages, Next Step)        │  │
│  └───────────────────────────────┘  │
│                                     │
│  ┌─────────┐    ┌──────────────┐  │
│  │  Agent  │───▶│    Tools     │  │
│  │  Node   │◀───│    Node      │  │
│  └─────────┘    └──────────────┘  │
│       │                             │
│       ▼                             │
│  ┌──────────┐                      │
│  │   END    │                      │
│  └──────────┘                      │
└─────────────────────────────────────┘
       │
       ▼
┌──────────────┐
│   Response   │
└──────────────┘
```

### LangGraph Concepts Demonstrated:

1. **StateGraph**: Defines the workflow structure
2. **State Management**: Uses TypedDict to track conversation messages
3. **Nodes**: Discrete processing steps (agent, tools)
4. **Edges**: Flow control between nodes
5. **Conditional Routing**: Dynamic decision-making based on state
6. **Tool Integration**: Binding and executing tools from the LLM

## 🚀 Setup Instructions

### Prerequisites

- **Dev Container**: This project runs in a dev container
- **Ollama**: Running on your host machine with models pulled
- **Python 3.12+**: Included in the dev container

### Step 1: Verify Ollama on Host

On your host machine, ensure Ollama is running and has models:

```bash
# Check Ollama status
ollama list

# Pull a model with tool calling support (RECOMMENDED)
ollama pull llama3.2    # 2GB - Fast, supports tools
# OR
ollama pull qwen2.5:3b  # 2GB - Fast, supports tools
# OR
ollama pull llama3.1    # Larger but very capable

# Note: Older models like llama3:8b work but without native tool calling
```

### Step 2: Configure Connection

The default configuration assumes Ollama is accessible at `http://host.docker.internal:11434`. For Linux hosts using default Docker networking, you may need to change this to `http://172.17.0.1:11434`.

Create a `.env` file (optional):

```bash
cp .env.example .env
# Edit .env to customize settings
```

Or export environment variables:

```bash
export OLLAMA_BASE_URL=http://host.docker.internal:11434
export OLLAMA_MODEL=llama3.2
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

## 📖 Usage

### Interactive Mode

Run the agent in interactive mode for a conversational experience:

```bash
python agent.py
```

Example session:
```
You: What is quantum computing?
[Agent searches Wikipedia and provides answer]

You: Calculate 15% of 240
[Agent uses calculator tool]

You: Who invented Python and what year?
[Agent searches and provides information]
```

### Example Scripts

Run pre-defined examples to see the agent in action:

```bash
python main.py
```

This provides:
1. Simple Wikipedia search
2. Mathematical calculations
3. Multi-step reasoning
4. Current information queries
5. Complex multi-tool queries

### Programmatic Usage

```python
from agent import run_agent

# Run a single query
response = run_agent("What is machine learning?", verbose=True)
print(response)
```

## 🔧 Configuration

Edit [config.py](config.py) to customize:

- **OLLAMA_BASE_URL**: Connection URL to Ollama
- **DEFAULT_MODEL**: Which Ollama model to use
- **MAX_ITERATIONS**: Maximum agent iterations
- **RECURSION_LIMIT**: Graph recursion limit

## 🛠️ Available Tools

### 1. Wikipedia Search
Searches Wikipedia and returns summarized information.

```python
"What is the history of the Internet?"
```

**Note**: The agent is configured to prioritize Wikipedia searches for factual information rather than relying on the LLM's internal knowledge. This ensures accuracy for queries involving numbers, dates, statistics, and other verifiable facts.

### 2. Calculator
Performs mathematical calculations safely.

```python
"What is (123 + 456) * 789 / 12?"
```

### 3. Current Time
Gets the current date and time.

```python
"What time is it now?"
```

## 🎯 Fact-Checking & Tool Usage Strategy

This agent implements a **fact-first approach** to ensure accuracy:

### System Prompt Design
The agent includes a system message that instructs it to:
1. **Always verify facts** - Search Wikipedia for numbers, statistics, dates
2. **Never rely on internal knowledge** - Use tools to verify information
3. **Break down complex queries** - Search first, then calculate

### Example Behavior
**Query**: "Find the number of states in the US, add to the number of states in Brazil, then multiply them together"

**Agent's approach**:
1. 🔍 Calls `wikipedia_search("United States")` → Finds 50 states
2. 🔍 Calls `wikipedia_search("Brazil states")` → Finds 26 states  
3. 🧮 Calls `calculator("(50 + 26) * (50 * 26)")` → Computes result

This prevents the agent from using potentially outdated training data and ensures current, accurate information.

### Why This Matters
Without the fact-checking prompt, LLMs tend to use their internal knowledge, which can be:
- Outdated (training data cutoff)
- Incorrect (hallucinations)
- Unverifiable (no source)

By forcing Wikipedia lookups, the agent provides **verifiable, sourced answers**

## 📚 Learning Points

This project demonstrates:

### LangGraph Concepts
- **Graph Construction**: Building workflows with nodes and edges
- **State Management**: Maintaining conversation context
- **Conditional Routing**: Dynamic flow control based on state
- **Tool Integration**: Connecting LLM with external tools
- **Streaming**: Processing agent steps incrementally

### LangChain Concepts
- **Messages**: HumanMessage, AIMessage, ToolMessage
- **Tool Binding**: Connecting functions to LLM
- **Chat Models**: Using Ollama through LangChain

### Agent Patterns
- **ReAct Pattern**: Reasoning and Acting in cycles
- **Tool Selection**: LLM choosing appropriate tools
- **Multi-step Reasoning**: Breaking complex queries into steps

## 🔍 Example Queries to Try

1. **Simple Fact-Finding**:
   - "Who is the current president of France?"
   - "What is the capital of Australia?"

2. **Calculations**:
   - "If I save $500 per month, how much will I have in 3 years?"
   - "What is 25% of 890?"

3. **Multi-Step Reasoning**:
   - "Search for information about Ada Lovelace and calculate how many years ago she lived"
   - "What is Python programming language and how many years has it been since release?"

4. **Time-Based**:
   - "What is the current date and time?"
   - "How many days until the end of the year?"

## 🐛 Troubleshooting

### Connection Issues

If the agent can't connect to Ollama:

**Linux (default bridge network)**:
```bash
export OLLAMA_BASE_URL=http://172.17.0.1:11434
```

**Alternative: Use host network** (modify `.devcontainer/devcontainer.json`):
```json
"runArgs": ["--network=host"]
```
Then use `http://localhost:11434`

### Verify Ollama Connection

```bash
curl http://host.docker.internal:11434/api/tags
```

Should return a list of available models.

### Model Not Found

Ensure you've pulled the model on your host:
```bash
ollama pull llama3.2
```

## 📖 Further Learning

- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [LangChain Documentation](https://python.langchain.com/)
- [Ollama Documentation](https://ollama.ai/docs)

## 📝 License

This is a learning project - feel free to use and modify as needed!