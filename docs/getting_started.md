# Getting Started with Agent Development

This guide will help you get started with building autonomous agents using this framework.

## Installation

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone https://github.com/soandersson/agentpoc.git
cd agentpoc
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Verify installation:
```bash
python -m pytest tests/
```

## Your First Agent

Let's create a simple reactive agent that responds to temperature readings.

### Step 1: Import Required Classes

```python
from src.core import Observation, Action
from src.agents.reactive_agent import ReactiveAgent
import time
```

### Step 2: Create the Agent

```python
# Create a thermostat agent
agent = ReactiveAgent("ThermostatAgent")
```

### Step 3: Define Rules

```python
# Define what to do when it's too hot
def handle_hot(data):
    return Action(
        name="cool_down",
        parameters={'target_temp': 20},
        confidence=1.0
    )

# Define what to do when it's too cold
def handle_cold(data):
    return Action(
        name="heat_up",
        parameters={'target_temp': 20},
        confidence=1.0
    )

# Register the rules
agent.add_rule('hot', handle_hot)
agent.add_rule('cold', handle_cold)
```

### Step 4: Run the Agent

```python
# Create an observation
observation = Observation(
    data={'type': 'hot', 'temperature': 28},
    timestamp=time.time()
)

# Run agent cycle
result = agent.run_cycle(observation)
print(f"Action taken: {result['action']}")
print(f"Parameters: {result['parameters']}")
```

Output:
```
Action taken: cool_down
Parameters: {'target_temp': 20}
```

## Creating a Learning Agent

Now let's create an agent that learns from experience.

### Step 1: Import and Create

```python
from src.core import Observation
from src.agents.qlearning_agent import QLearningAgent

agent = QLearningAgent(
    name="LearningBot",
    actions=['forward', 'backward', 'left', 'right'],
    learning_rate=0.1,
    discount_factor=0.9,
    exploration_rate=0.2
)
```

### Step 2: Training Loop

```python
# Training loop
for episode in range(100):
    # Reset environment (your code here)
    
    while not done:
        # Get observation
        obs = Observation(data=current_state, timestamp=time.time())
        
        # Agent perceives and decides
        agent.perceive(obs)
        action = agent.decide()
        
        # Execute action in environment
        reward = environment.step(action.name)
        
        # Agent learns
        agent.learn(reward)
        
        if reached_goal:
            break
```

### Step 3: Evaluate

```python
# Check learning progress
summary = agent.get_q_table_summary()
print(f"States visited: {summary['states_visited']}")
print(f"Average Q-value: {summary['average_q_value']:.2f}")
```

## Running Examples

The repository includes complete examples:

### Simple Reactive Agent
```bash
python examples/simple_agent.py
```

This demonstrates a thermostat agent responding to temperature changes.

### Q-Learning Agent
```bash
python examples/learning_agent_example.py
```

This shows an agent learning to navigate a grid world.

## Understanding Agent States

Agents maintain state throughout their lifecycle:

- **IDLE**: Ready to receive observations
- **THINKING**: Processing observations and making decisions
- **ACTING**: Executing actions
- **LEARNING**: Updating internal models (learning agents only)

Check agent state:
```python
print(agent.state)  # AgentState.IDLE
```

## Key Concepts

### Observations
Data from the environment that agents perceive:
```python
obs = Observation(
    data={'sensor': 'value'},
    timestamp=time.time(),
    metadata={'source': 'sensor_1'}
)
```

### Actions
Decisions made by agents:
```python
action = Action(
    name='move',
    parameters={'direction': 'north', 'speed': 5},
    confidence=0.85
)
```

### The Perception-Decision-Action Loop

Every agent follows this cycle:
1. **Perceive**: Process environmental observations
2. **Decide**: Choose an action based on current state
3. **Act**: Execute the chosen action
4. **Learn** (optional): Update internal models based on feedback

## Testing Your Agent

Create tests to verify agent behavior:

```python
import pytest
from src.core import Observation, Action
from src.agents.reactive_agent import ReactiveAgent

def test_agent_responds_correctly():
    agent = ReactiveAgent("TestAgent")
    
    def rule(data):
        return Action(name="response", parameters={})
    
    agent.add_rule("trigger", rule)
    
    obs = Observation(data={"type": "trigger"}, timestamp=0)
    result = agent.run_cycle(obs)
    
    assert result['action'] == "response"
```

Run tests:
```bash
pytest tests/
```

## Next Steps

1. **Explore the examples** in the `examples/` directory
2. **Read the architecture documentation** in `docs/architecture.md`
3. **Review the API reference** in `docs/api_reference.md`
4. **Create your own agent** for a specific problem
5. **Experiment with different learning parameters** to optimize performance

## Common Issues

### Import Errors
Make sure you're running from the project root directory:
```bash
cd /path/to/agentpoc
python examples/simple_agent.py
```

### Agent Not Learning
Check these parameters:
- Learning rate too low? Try 0.1 - 0.3
- Exploration rate too high? Try 0.1 - 0.2
- Discount factor? Usually 0.8 - 0.99

### Slow Performance
- Reduce observation history size
- Limit Q-table entries
- Use more efficient state representations

## Getting Help

- Review the examples in `examples/`
- Check the architecture documentation
- Look at the test files for usage patterns

## Contributing

Feel free to extend the framework:
1. Add new agent types
2. Implement different learning algorithms
3. Create new examples
4. Improve documentation

Happy agent building!
