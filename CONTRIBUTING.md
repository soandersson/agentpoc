# Contributing to Agent Development POC

Thank you for your interest in contributing to this project! This document provides guidelines for contributing.

## Getting Started

1. Fork the repository
2. Clone your fork
3. Create a new branch for your feature
4. Make your changes
5. Run tests
6. Submit a pull request

## Development Setup

```bash
# Clone the repository
git clone https://github.com/soandersson/agentpoc.git
cd agentpoc

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/

# Run tests with coverage
pytest --cov=src tests/
```

## Code Style

- Follow PEP 8 style guidelines
- Use type hints for function parameters and returns
- Write docstrings for all public classes and methods
- Keep functions focused and single-purpose

## Testing

- Write tests for all new functionality
- Ensure all tests pass before submitting PR
- Aim for >90% code coverage
- Test edge cases and error conditions

## Documentation

- Update README.md if adding new features
- Add docstrings following Google style
- Update API reference if changing public interfaces
- Include examples for new agent types

## Pull Request Process

1. Update documentation as needed
2. Add tests for new functionality
3. Ensure all tests pass
4. Update the README with details of changes
5. The PR will be reviewed and merged if approved

## Adding New Agent Types

When adding a new agent implementation:

1. Inherit from BaseAgent or LearningAgent
2. Implement required abstract methods
3. Add comprehensive tests
4. Include usage examples
5. Document the agent's purpose and behavior

Example:
```python
from src.core import BaseAgent, Observation, Action

class MyNewAgent(BaseAgent):
    """
    Brief description of the agent.
    
    Detailed explanation of behavior and use cases.
    """
    
    def perceive(self, observation: Observation) -> None:
        # Implementation
        pass
    
    def decide(self) -> Optional[Action]:
        # Implementation
        pass
    
    def act(self, action: Action) -> Any:
        # Implementation
        pass
```

## Adding New Examples

Examples should:
- Be self-contained and runnable
- Include clear comments
- Demonstrate real-world use cases
- Show best practices

## Reporting Issues

When reporting issues:
- Describe the expected behavior
- Describe the actual behavior
- Include code to reproduce
- Specify Python version and dependencies

## Questions?

Feel free to open an issue for questions or suggestions.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
