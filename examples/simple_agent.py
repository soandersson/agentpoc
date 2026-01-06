"""
Simple Reactive Agent Example

This example demonstrates a basic reactive agent that responds to temperature readings.
"""

import time
from src.core import Observation, Action
from src.agents.reactive_agent import ReactiveAgent


def main():
    """Run a simple reactive agent example."""
    print("=== Simple Reactive Agent Example ===\n")
    
    # Create a temperature monitoring agent
    agent = ReactiveAgent("ThermostatAgent")
    
    # Define condition-action rules
    def handle_hot(data):
        temp = data.get('temperature', 0)
        return Action(
            name="cool_down",
            parameters={'target_temp': 20, 'current_temp': temp},
            confidence=1.0
        )
    
    def handle_cold(data):
        temp = data.get('temperature', 0)
        return Action(
            name="heat_up",
            parameters={'target_temp': 20, 'current_temp': temp},
            confidence=1.0
        )
    
    def handle_comfortable(data):
        return Action(
            name="maintain",
            parameters={'message': 'Temperature is optimal'},
            confidence=1.0
        )
    
    # Register rules
    agent.add_rule('hot', handle_hot)
    agent.add_rule('cold', handle_cold)
    agent.add_rule('comfortable', handle_comfortable)
    
    # Simulate temperature readings
    scenarios = [
        {'type': 'hot', 'temperature': 28},
        {'type': 'cold', 'temperature': 15},
        {'type': 'comfortable', 'temperature': 21},
        {'type': 'hot', 'temperature': 30},
        {'type': 'comfortable', 'temperature': 20},
    ]
    
    print("Simulating temperature monitoring...\n")
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"Scenario {i}:")
        print(f"  Input: {scenario}")
        
        # Create observation
        obs = Observation(
            data=scenario,
            timestamp=time.time()
        )
        
        # Run agent cycle
        result = agent.run_cycle(obs)
        
        print(f"  Agent State: {agent.state.value}")
        print(f"  Action Taken: {result['action']}")
        print(f"  Parameters: {result['parameters']}")
        print()
    
    # Summary
    print(f"\nAgent Summary:")
    print(f"  Total observations: {len(agent.observations)}")
    print(f"  Total actions taken: {len(agent.actions_taken)}")
    print(f"  Actions: {[a.name for a in agent.actions_taken]}")


if __name__ == "__main__":
    main()
