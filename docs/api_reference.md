# API Reference

Complete API documentation for the agent development framework.

## Core Module (`src.core`)

### BaseAgent

Abstract base class for all agents.

#### Constructor

```python
BaseAgent(name: str)
```

**Parameters:**
- `name`: Unique identifier for the agent

**Attributes:**
- `name`: str - Agent identifier
- `state`: AgentState - Current agent state
- `observations`: List[Observation] - History of observations
- `actions_taken`: List[Action] - History of actions

#### Methods

##### perceive()
```python
@abstractmethod
def perceive(self, observation: Observation) -> None
```
Process an observation from the environment.

**Parameters:**
- `observation`: The observation to process

**Returns:** None

---

##### decide()
```python
@abstractmethod
def decide(self) -> Optional[Action]
```
Make a decision based on current state and observations.

**Returns:** An Action to take, or None if no action is needed

---

##### act()
```python
@abstractmethod
def act(self, action: Action) -> Any
```
Execute an action in the environment.

**Parameters:**
- `action`: The action to execute

**Returns:** The result of the action

---

##### run_cycle()
```python
def run_cycle(self, observation: Observation) -> Optional[Any]
```
Execute one complete perception-decision-action cycle.

**Parameters:**
- `observation`: The current observation from the environment

**Returns:** The result of the action, if any

---

##### reset()
```python
def reset(self) -> None
```
Reset the agent to its initial state.

**Returns:** None

---

### LearningAgent

Base class for agents that can learn from experience. Extends BaseAgent.

#### Constructor

```python
LearningAgent(name: str, learning_rate: float = 0.1)
```

**Parameters:**
- `name`: Unique identifier for the agent
- `learning_rate`: Rate at which the agent learns (0.0 to 1.0)

**Additional Attributes:**
- `learning_rate`: float - Learning rate parameter
- `experience`: List[Dict[str, Any]] - History of learning experiences

#### Methods

##### learn()
```python
@abstractmethod
def learn(self, reward: float) -> None
```
Learn from the result of an action.

**Parameters:**
- `reward`: Feedback signal indicating success/failure

**Returns:** None

---

##### run_cycle_with_feedback()
```python
def run_cycle_with_feedback(
    self, 
    observation: Observation, 
    reward: Optional[float] = None
) -> Optional[Any]
```
Execute a cycle with learning feedback.

**Parameters:**
- `observation`: The current observation
- `reward`: Optional feedback from previous action

**Returns:** The result of the action, if any

---

### Observation

Dataclass representing an observation from the environment.

```python
@dataclass
class Observation:
    data: Any
    timestamp: float
    metadata: Optional[Dict[str, Any]] = None
```

**Attributes:**
- `data`: Any type - The observation payload
- `timestamp`: float - When the observation occurred
- `metadata`: Optional dict - Additional context

---

### Action

Dataclass representing an action taken by an agent.

```python
@dataclass
class Action:
    name: str
    parameters: Dict[str, Any]
    confidence: float = 1.0
```

**Attributes:**
- `name`: str - Action identifier
- `parameters`: Dict - Action-specific parameters
- `confidence`: float - Confidence level (0.0 to 1.0)

---

### AgentState

Enumeration of possible agent states.

```python
class AgentState(Enum):
    IDLE = "idle"
    THINKING = "thinking"
    ACTING = "acting"
    LEARNING = "learning"
    STOPPED = "stopped"
```

---

## Agents Module (`src.agents`)

### ReactiveAgent

A simple reactive agent that maps observations to actions using rules.

#### Constructor

```python
ReactiveAgent(name: str)
```

**Parameters:**
- `name`: Unique identifier for the agent

**Additional Attributes:**
- `rules`: Dict[str, Callable] - Condition-action mappings
- `default_action`: Optional[Action] - Default action when no rules match
- `current_observation`: Optional[Observation] - Most recent observation

#### Methods

##### add_rule()
```python
def add_rule(
    self, 
    condition: str, 
    action_fn: Callable[[Any], Action]
) -> None
```
Add a condition-action rule.

**Parameters:**
- `condition`: String key identifying the condition
- `action_fn`: Function that creates an action given observation data

**Returns:** None

**Example:**
```python
def handle_alert(data):
    return Action(name="respond", parameters={})

agent.add_rule("alert", handle_alert)
```

---

##### set_default_action()
```python
def set_default_action(self, action: Action) -> None
```
Set the default action when no rules match.

**Parameters:**
- `action`: The default action to take

**Returns:** None

---

### QLearningAgent

An agent that learns optimal actions using Q-learning.

#### Constructor

```python
QLearningAgent(
    name: str,
    actions: List[str],
    learning_rate: float = 0.1,
    discount_factor: float = 0.9,
    exploration_rate: float = 0.1
)
```

**Parameters:**
- `name`: Unique identifier for the agent
- `actions`: List of possible action names
- `learning_rate`: Rate at which to update Q-values (alpha), default 0.1
- `discount_factor`: Importance of future rewards (gamma), default 0.9
- `exploration_rate`: Probability of taking random action (epsilon), default 0.1

**Additional Attributes:**
- `available_actions`: List[str] - Possible actions
- `q_table`: Dict[Tuple[str, str], float] - Q-value mappings
- `current_state`: Optional[str] - Current state representation
- `last_state`: Optional[str] - Previous state
- `last_action`: Optional[str] - Last action taken

#### Methods

##### get_q_table_summary()
```python
def get_q_table_summary(self) -> Dict[str, Any]
```
Get a summary of the learned Q-table.

**Returns:** Dictionary with Q-table statistics:
- `total_entries`: Number of Q-table entries
- `total_experiences`: Number of learning experiences
- `average_q_value`: Mean Q-value
- `states_visited`: Number of unique states

**Example:**
```python
summary = agent.get_q_table_summary()
print(f"States visited: {summary['states_visited']}")
```

---

## Usage Examples

### Creating a Custom Agent

```python
from src.core import BaseAgent, Observation, Action

class MyAgent(BaseAgent):
    def perceive(self, observation: Observation):
        # Process observation
        self.observations.append(observation)
    
    def decide(self) -> Action:
        # Make decision
        return Action(name="my_action", parameters={})
    
    def act(self, action: Action):
        # Execute action
        return {"status": "success"}

# Use the agent
agent = MyAgent("CustomAgent")
obs = Observation(data="input", timestamp=0)
result = agent.run_cycle(obs)
```

### Using ReactiveAgent

```python
from src.agents.reactive_agent import ReactiveAgent
from src.core import Observation, Action

agent = ReactiveAgent("Bot")

# Add rules
agent.add_rule("event_a", lambda d: Action("respond_a", {}))
agent.add_rule("event_b", lambda d: Action("respond_b", {}))

# Set default
agent.set_default_action(Action("wait", {}))

# Run
obs = Observation(data={"type": "event_a"}, timestamp=0)
result = agent.run_cycle(obs)
```

### Using QLearningAgent

```python
from src.agents.qlearning_agent import QLearningAgent
from src.core import Observation

agent = QLearningAgent(
    name="Learner",
    actions=["up", "down", "left", "right"],
    learning_rate=0.1,
    exploration_rate=0.2
)

# Training loop
for episode in range(100):
    obs = Observation(data=get_state(), timestamp=0)
    agent.perceive(obs)
    
    action = agent.decide()
    if action:
        reward = execute_action(action.name)
        agent.learn(reward)

# Check results
summary = agent.get_q_table_summary()
```

---

## Type Hints

All functions use type hints for better IDE support:

```python
from typing import Any, Dict, List, Optional, Callable

def perceive(self, observation: Observation) -> None: ...
def decide(self) -> Optional[Action]: ...
def act(self, action: Action) -> Any: ...
```

---

## Error Handling

The framework uses standard Python exceptions. Common scenarios:

- **AttributeError**: Accessing attributes before initialization
- **KeyError**: Invalid rule condition or Q-table access
- **TypeError**: Invalid parameter types
- **ValueError**: Invalid parameter values

Always validate inputs in production code:

```python
if not isinstance(observation, Observation):
    raise TypeError("Expected Observation instance")
```

---

## Thread Safety

The current implementation is not thread-safe. For concurrent use:

1. Use separate agent instances per thread
2. Implement locking for shared resources
3. Consider using immutable data structures

---

## Performance Tips

### Memory Management
```python
# Clear observation history periodically
if len(agent.observations) > 1000:
    agent.observations = agent.observations[-100:]
```

### Efficient State Representation
```python
# Use tuples for hashable states
state = (position_x, position_y, health)

# Or simple strings
state = f"{x}_{y}_{health}"
```

### Q-Learning Optimization
```python
# Reduce exploration over time
agent.exploration_rate *= 0.99

# Limit Q-table size
max_table_size = 10000
if len(agent.q_table) > max_table_size:
    # Implement pruning strategy
    pass
```
