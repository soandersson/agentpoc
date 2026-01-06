"""
Reactive Agent Implementation

A simple agent that responds directly to stimuli without maintaining internal state.
"""

from typing import Optional, Callable, Dict, Any
from ..core import BaseAgent, Observation, Action


class ReactiveAgent(BaseAgent):
    """
    A simple reactive agent that maps observations to actions.
    
    This agent uses a set of condition-action rules to determine behavior.
    It does not maintain memory of past observations or learn from experience.
    """
    
    def __init__(self, name: str):
        """
        Initialize the reactive agent.
        
        Args:
            name: Unique identifier for the agent
        """
        super().__init__(name)
        self.rules: Dict[str, Callable[[Any], Action]] = {}
        self.default_action: Optional[Action] = None
        self.current_observation: Optional[Observation] = None
    
    def add_rule(
        self, 
        condition: str, 
        action_fn: Callable[[Any], Action]
    ) -> None:
        """
        Add a condition-action rule.
        
        Args:
            condition: A string key identifying the condition
            action_fn: Function that creates an action given observation data
        """
        self.rules[condition] = action_fn
    
    def set_default_action(self, action: Action) -> None:
        """
        Set the default action when no rules match.
        
        Args:
            action: The default action to take
        """
        self.default_action = action
    
    def perceive(self, observation: Observation) -> None:
        """
        Store the current observation.
        
        Args:
            observation: The observation to process
        """
        self.current_observation = observation
        self.observations.append(observation)
    
    def decide(self) -> Optional[Action]:
        """
        Decide on an action based on current observation.
        
        Returns:
            An Action if a rule matches, otherwise the default action
        """
        if not self.current_observation:
            return self.default_action
        
        # Check if observation data is a dict with a 'type' key
        if isinstance(self.current_observation.data, dict):
            obs_type = self.current_observation.data.get('type')
            if obs_type in self.rules:
                return self.rules[obs_type](self.current_observation.data)
        
        # Check if observation data directly matches a rule key
        if str(self.current_observation.data) in self.rules:
            return self.rules[str(self.current_observation.data)](
                self.current_observation.data
            )
        
        return self.default_action
    
    def act(self, action: Action) -> Any:
        """
        Execute the action.
        
        Args:
            action: The action to execute
            
        Returns:
            A result dictionary
        """
        return {
            'agent': self.name,
            'action': action.name,
            'parameters': action.parameters,
            'success': True
        }
