# Best Practices for Agent Development

This guide covers best practices and design patterns for building robust, maintainable agents.

## Core Principles

### 1. Single Responsibility Principle

Each agent should have a single, well-defined purpose:

**Good:**
```python
class TemperatureControlAgent(ReactiveAgent):
    """Manages temperature control only."""
    pass

class HumidityControlAgent(ReactiveAgent):
    """Manages humidity control only."""
    pass
```

**Avoid:**
```python
class ClimateAgent(ReactiveAgent):
    """Manages temperature, humidity, air quality, etc."""
    # Too many responsibilities!
    pass
```

### 2. Separation of Concerns

Keep perception, decision-making, and action execution separate:

```python
def perceive(self, observation):
    # Only process input - no decisions or actions
    self.current_state = self._extract_state(observation)

def decide(self):
    # Only make decisions - no perception or execution
    return self._select_best_action()

def act(self, action):
    # Only execute - no perception or decisions
    return self._execute(action)
```

### 3. Immutability

Avoid modifying observations or shared state:

**Good:**
```python
def perceive(self, observation):
    # Store, don't modify
    self.observations.append(observation)
    new_state = self._compute_state(observation.data)
```

**Avoid:**
```python
def perceive(self, observation):
    # Don't modify the observation!
    observation.data['processed'] = True
```

## Design Patterns

### 1. Strategy Pattern for Decision Making

Allow different decision strategies to be plugged in:

```python
class Agent:
    def __init__(self, decision_strategy):
        self.decision_strategy = decision_strategy
    
    def decide(self):
        return self.decision_strategy.select_action(self.current_state)

# Different strategies
class GreedyStrategy:
    def select_action(self, state):
        return best_immediate_action(state)

class LookaheadStrategy:
    def select_action(self, state):
        return best_future_action(state)
```

### 2. Observer Pattern for State Changes

Notify interested parties when agent state changes:

```python
class Agent:
    def __init__(self):
        self.observers = []
    
    def attach(self, observer):
        self.observers.append(observer)
    
    def notify(self, event):
        for observer in self.observers:
            observer.update(self, event)
    
    def perceive(self, observation):
        self.current_state = observation
        self.notify('state_changed')
```

### 3. Template Method Pattern

Already used in BaseAgent - subclasses implement specifics:

```python
class BaseAgent:
    def run_cycle(self, observation):
        # Template - defines algorithm structure
        self.perceive(observation)      # Step 1
        action = self.decide()          # Step 2
        if action:
            return self.act(action)     # Step 3
    
    @abstractmethod
    def perceive(self, observation):
        # Subclass implements
        pass
```

## Testing Best Practices

### 1. Test in Isolation

Test each component independently:

```python
def test_perception():
    agent = MyAgent()
    obs = Observation(data="test", timestamp=0)
    agent.perceive(obs)
    assert agent.current_state == expected_state

def test_decision():
    agent = MyAgent()
    agent.current_state = known_state
    action = agent.decide()
    assert action.name == expected_action
```

### 2. Use Mock Objects

Mock environment interactions:

```python
from unittest.mock import Mock

def test_agent_with_mock_environment():
    mock_env = Mock()
    mock_env.get_observation.return_value = Observation(...)
    
    agent = MyAgent()
    agent.environment = mock_env
    
    agent.run_cycle()
    mock_env.get_observation.assert_called_once()
```

### 3. Test Edge Cases

Always test boundary conditions:

```python
def test_empty_observation():
    agent = MyAgent()
    obs = Observation(data=None, timestamp=0)
    # Should handle gracefully
    agent.perceive(obs)
    assert agent.current_state is not None

def test_invalid_action():
    agent = MyAgent()
    # What happens with invalid input?
    result = agent.act(Action(name="invalid", parameters={}))
    # Should return error or default behavior
```

## Performance Optimization

### 1. Limit History Size

Prevent unbounded memory growth:

```python
class Agent:
    def __init__(self, max_history=100):
        self.max_history = max_history
        self.observations = []
    
    def perceive(self, observation):
        self.observations.append(observation)
        if len(self.observations) > self.max_history:
            self.observations = self.observations[-self.max_history:]
```

### 2. Cache Expensive Computations

```python
class Agent:
    def __init__(self):
        self._state_cache = {}
    
    def _compute_state(self, observation):
        key = self._make_key(observation)
        if key not in self._state_cache:
            self._state_cache[key] = expensive_computation(observation)
        return self._state_cache[key]
```

### 3. Use Efficient Data Structures

```python
# Good - O(1) lookup
self.q_table = {}  # dict

# Avoid - O(n) lookup
self.q_table = []  # list
```

## Error Handling

### 1. Validate Inputs

```python
def perceive(self, observation):
    if not isinstance(observation, Observation):
        raise TypeError("Expected Observation instance")
    
    if observation.data is None:
        raise ValueError("Observation data cannot be None")
    
    # Process observation
    ...
```

### 2. Provide Meaningful Error Messages

```python
# Good
raise ValueError(
    f"Action '{action.name}' not in available actions: "
    f"{self.available_actions}"
)

# Avoid
raise ValueError("Invalid action")
```

### 3. Handle Failures Gracefully

```python
def act(self, action):
    try:
        return self._execute_action(action)
    except Exception as e:
        self.logger.error(f"Action failed: {e}")
        return self._get_default_result()
```

## Code Organization

### 1. Clear Module Structure

```
src/
├── core/           # Base classes and abstractions
├── agents/         # Agent implementations
├── environments/   # Environment simulations
├── strategies/     # Decision strategies
└── utils/          # Helper functions
```

### 2. Consistent Naming

```python
# Classes: PascalCase
class ReactiveAgent:
    pass

# Functions/Methods: snake_case
def compute_reward(state, action):
    pass

# Constants: UPPER_SNAKE_CASE
MAX_ITERATIONS = 1000
```

### 3. Comprehensive Documentation

```python
def learn(self, reward: float) -> None:
    """
    Update internal model based on received reward.
    
    This method implements the Q-learning update rule to improve
    the agent's policy over time.
    
    Args:
        reward: Numerical feedback signal. Positive values indicate
                good outcomes, negative values indicate bad outcomes.
    
    Returns:
        None
    
    Raises:
        ValueError: If reward is NaN or infinite
    
    Example:
        >>> agent.learn(10.0)  # Good outcome
        >>> agent.learn(-5.0)  # Bad outcome
    """
    ...
```

## Learning Agent Best Practices

### 1. Balance Exploration and Exploitation

```python
# Decrease exploration over time
def update_exploration_rate(self, episode):
    self.exploration_rate = max(
        0.01,  # minimum exploration
        self.exploration_rate * 0.995  # decay factor
    )
```

### 2. Use Appropriate Learning Rates

```python
# Higher learning rate for dynamic environments
agent = QLearningAgent(learning_rate=0.3)

# Lower learning rate for stable environments
agent = QLearningAgent(learning_rate=0.1)
```

### 3. Monitor Learning Progress

```python
class LearningAgent:
    def __init__(self):
        self.performance_history = []
    
    def log_performance(self, episode, reward):
        self.performance_history.append({
            'episode': episode,
            'reward': reward,
            'avg_reward': self._compute_average(50)
        })
    
    def _compute_average(self, window):
        recent = self.performance_history[-window:]
        return sum(r['reward'] for r in recent) / len(recent)
```

## Security Considerations

### 1. Validate External Input

```python
def perceive(self, observation):
    # Sanitize observation data
    if isinstance(observation.data, dict):
        # Remove potentially dangerous keys
        safe_data = {
            k: v for k, v in observation.data.items()
            if k not in ['__class__', '__dict__']
        }
        observation.data = safe_data
```

### 2. Limit Resource Usage

```python
class Agent:
    def __init__(self, max_memory_mb=100):
        self.max_memory_mb = max_memory_mb
    
    def perceive(self, observation):
        if self._get_memory_usage() > self.max_memory_mb:
            self._cleanup_old_data()
        # Continue processing
```

### 3. Avoid Code Injection

```python
# Never use eval() or exec() on user input
# Bad:
action_name = eval(user_input)  # DON'T DO THIS

# Good:
action_name = str(user_input)
if action_name not in self.valid_actions:
    raise ValueError(f"Invalid action: {action_name}")
```

## Debugging Tips

### 1. Add Logging

```python
import logging

class Agent:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def decide(self):
        self.logger.debug(f"Current state: {self.current_state}")
        action = self._select_action()
        self.logger.info(f"Selected action: {action.name}")
        return action
```

### 2. Track State History

```python
class Agent:
    def __init__(self, debug=False):
        self.debug = debug
        self.state_history = []
    
    def perceive(self, observation):
        if self.debug:
            self.state_history.append({
                'timestamp': time.time(),
                'observation': observation,
                'state_before': self.current_state
            })
        # Normal processing
```

### 3. Use Assertions

```python
def decide(self):
    action = self._compute_best_action()
    
    # Sanity check
    assert action is not None, "Action should never be None"
    assert action.name in self.available_actions, \
        f"Invalid action: {action.name}"
    
    return action
```

## Deployment Considerations

### 1. Configuration Management

```python
# config.py
class AgentConfig:
    learning_rate: float = 0.1
    exploration_rate: float = 0.2
    max_history: int = 1000
    
# agent.py
class Agent:
    def __init__(self, config: AgentConfig):
        self.config = config
        self.learning_rate = config.learning_rate
```

### 2. Versioning

```python
class Agent:
    VERSION = "1.0.0"
    
    def save_checkpoint(self, path):
        checkpoint = {
            'version': self.VERSION,
            'state': self.get_state(),
            'q_table': self.q_table
        }
        # Save checkpoint
```

### 3. Monitoring

```python
class Agent:
    def __init__(self):
        self.metrics = {
            'total_decisions': 0,
            'successful_actions': 0,
            'errors': 0
        }
    
    def decide(self):
        self.metrics['total_decisions'] += 1
        # Make decision
```

## Summary

Key takeaways:
1. Keep components separate and focused
2. Test thoroughly, including edge cases
3. Optimize for maintainability first, performance second
4. Document your code and decisions
5. Monitor and log agent behavior
6. Validate all inputs
7. Handle errors gracefully
