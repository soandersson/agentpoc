"""
Q-Learning Agent Implementation

A learning agent that uses Q-learning to improve decision-making over time.
"""

from typing import Optional, List, Tuple, Dict, Any
from collections import defaultdict
import random
from ..core import LearningAgent, Observation, Action


class QLearningAgent(LearningAgent):
    """
    An agent that learns optimal actions using Q-learning.
    
    This agent maintains a Q-table that maps state-action pairs to expected rewards.
    It explores the environment while gradually exploiting learned knowledge.
    """
    
    def __init__(
        self,
        name: str,
        actions: List[str],
        learning_rate: float = 0.1,
        discount_factor: float = 0.9,
        exploration_rate: float = 0.1
    ):
        """
        Initialize the Q-learning agent.
        
        Args:
            name: Unique identifier for the agent
            actions: List of possible action names
            learning_rate: Rate at which to update Q-values (alpha)
            discount_factor: Importance of future rewards (gamma)
            exploration_rate: Probability of taking random action (epsilon)
        """
        super().__init__(name, learning_rate)
        self.available_actions = actions
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        
        # Q-table: maps (state, action) to expected reward
        self.q_table: Dict[Tuple[str, str], float] = defaultdict(float)
        
        # Track current state and last action for learning
        self.current_state: Optional[str] = None
        self.last_state: Optional[str] = None
        self.last_action: Optional[str] = None
        self.last_reward: float = 0.0
    
    def _state_from_observation(self, observation: Observation) -> str:
        """
        Convert an observation into a state representation.
        
        Args:
            observation: The observation to convert
            
        Returns:
            A string representation of the state
        """
        if isinstance(observation.data, dict):
            # Create a simple string key from dict
            return str(sorted(observation.data.items()))
        return str(observation.data)
    
    def perceive(self, observation: Observation) -> None:
        """
        Process an observation and update current state.
        
        Args:
            observation: The observation to process
        """
        self.observations.append(observation)
        self.last_state = self.current_state
        self.current_state = self._state_from_observation(observation)
    
    def decide(self) -> Optional[Action]:
        """
        Choose an action using epsilon-greedy strategy.
        
        Returns:
            An Action based on Q-values or random exploration
        """
        if not self.current_state:
            return None
        
        # Epsilon-greedy action selection
        if random.random() < self.exploration_rate:
            # Explore: choose random action
            action_name = random.choice(self.available_actions)
        else:
            # Exploit: choose best known action
            action_name = self._get_best_action(self.current_state)
        
        self.last_action = action_name
        
        return Action(
            name=action_name,
            parameters={},
            confidence=1.0 - self.exploration_rate
        )
    
    def _get_best_action(self, state: str) -> str:
        """
        Get the action with highest Q-value for a state.
        
        Args:
            state: The state to evaluate
            
        Returns:
            The action name with highest expected reward
        """
        q_values = [
            self.q_table[(state, action)] 
            for action in self.available_actions
        ]
        
        if max(q_values) == min(q_values):
            # All equal, choose randomly
            return random.choice(self.available_actions)
        
        max_q = max(q_values)
        best_actions = [
            action for action, q in zip(self.available_actions, q_values)
            if q == max_q
        ]
        return random.choice(best_actions)
    
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
            'state': self.current_state,
            'q_value': self.q_table.get(
                (self.current_state, action.name), 0.0
            )
        }
    
    def learn(self, reward: float) -> None:
        """
        Update Q-values based on received reward.
        
        Args:
            reward: The reward received for the last action
        """
        if not self.last_state or not self.last_action:
            return
        
        # Q-learning update rule:
        # Q(s,a) = Q(s,a) + α * [r + γ * max(Q(s',a')) - Q(s,a)]
        
        old_q = self.q_table[(self.last_state, self.last_action)]
        
        # Get maximum Q-value for next state
        if self.current_state:
            next_max_q = max(
                self.q_table[(self.current_state, action)]
                for action in self.available_actions
            )
        else:
            next_max_q = 0.0
        
        # Calculate new Q-value
        new_q = old_q + self.learning_rate * (
            reward + self.discount_factor * next_max_q - old_q
        )
        
        self.q_table[(self.last_state, self.last_action)] = new_q
        
        # Store experience
        self.experience.append({
            'state': self.last_state,
            'action': self.last_action,
            'reward': reward,
            'next_state': self.current_state,
            'q_value': new_q
        })
    
    def get_q_table_summary(self) -> Dict[str, Any]:
        """
        Get a summary of the learned Q-table.
        
        Returns:
            Dictionary with Q-table statistics
        """
        return {
            'total_entries': len(self.q_table),
            'total_experiences': len(self.experience),
            'average_q_value': (
                sum(self.q_table.values()) / len(self.q_table)
                if self.q_table else 0.0
            ),
            'states_visited': len(set(
                state for state, _ in self.q_table.keys()
            ))
        }
