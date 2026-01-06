# Agent Development Learning POC

A proof-of-concept repository for learning agent development concepts, patterns, and implementations.

## Overview

This repository provides a foundational framework for understanding and developing autonomous agents. It includes:

- **Agent Base Classes**: Core abstractions for building different types of agents
- **Example Implementations**: Practical examples of reactive and learning agents
- **Documentation**: Comprehensive guides and tutorials
- **Testing Framework**: Unit and integration tests

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/soandersson/agentpoc.git
cd agentpoc

# Install dependencies
pip install -r requirements.txt
```

### Running Examples

Using the CLI runner:
```bash
# Run a simple reactive agent
python run_example.py simple

# Run a learning agent example
python run_example.py learning

# Get help
python run_example.py --help
```

Or run examples directly:
```bash
# Run with PYTHONPATH
PYTHONPATH=. python examples/simple_agent.py
PYTHONPATH=. python examples/learning_agent_example.py
```

## Project Structure

```
agentpoc/
├── src/               # Core agent framework
│   ├── agents/        # Agent implementations
│   └── core/          # Base classes and utilities
├── examples/          # Example usage and demos
├── tests/             # Test suite
├── docs/              # Documentation and guides
└── README.md          # This file
```

## Agent Types

### Reactive Agents
Simple agents that respond directly to environmental stimuli without internal state or learning capabilities.

### Learning Agents
Agents that improve their performance over time through experience and feedback.

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src tests/
```

## Documentation

See the [docs](./docs) directory for:
- Architecture overview
- Agent design patterns
- API reference
- Best practices

## Contributing

This is a learning project. Feel free to experiment and extend the functionality.

## License

MIT License