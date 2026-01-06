"""
Core Agent Framework

This module provides the foundational classes for building autonomous agents.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from dataclasses import dataclass
from enum import Enum


class AgentState(Enum):
    """Enumeration of possible agent states."""
    IDLE = "idle"
    THINKING = "thinking"
    ACTING = "acting"
    LEARNING = "learning"
    STOPPED = "stopped"


@dataclass
class Observation:
    """Represents an observation from the environment."""
    data: Any
    timestamp: float
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class Action:
    """Represents an action taken by an agent."""
    name: str
    parameters: Dict[str, Any]
    confidence: float = 1.0


class BaseAgent(ABC):
    """
    Abstract base class for all agents.
    
    This class defines the core interface that all agents must implement.
    It provides the basic structure for perception, decision-making, and action.
    """
    
    def __init__(self, name: str):
        """
        Initialize the agent.
        
        Args:
            name: A unique identifier for the agent
        """
        self.name = name
        self.state = AgentState.IDLE
        self.observations: List[Observation] = []
        self.actions_taken: List[Action] = []
        
    @abstractmethod
    def perceive(self, observation: Observation) -> None:
        """
        Process an observation from the environment.
        
        Args:
            observation: The observation to process
        """
        pass
    
    @abstractmethod
    def decide(self) -> Optional[Action]:
        """
        Make a decision based on current state and observations.
        
        Returns:
            An Action to take, or None if no action is needed
        """
        pass
    
    @abstractmethod
    def act(self, action: Action) -> Any:
        """
        Execute an action in the environment.
        
        Args:
            action: The action to execute
            
        Returns:
            The result of the action
        """
        pass
    
    def run_cycle(self, observation: Observation) -> Optional[Any]:
        """
        Execute one complete perception-decision-action cycle.
        
        Args:
            observation: The current observation from the environment
            
        Returns:
            The result of the action, if any
        """
        self.state = AgentState.THINKING
        self.perceive(observation)
        
        action = self.decide()
        
        if action:
            self.state = AgentState.ACTING
            result = self.act(action)
            self.actions_taken.append(action)
            self.state = AgentState.IDLE
            return result
        
        self.state = AgentState.IDLE
        return None
    
    def reset(self) -> None:
        """Reset the agent to its initial state."""
        self.state = AgentState.IDLE
        self.observations.clear()
        self.actions_taken.clear()


class LearningAgent(BaseAgent):
    """
    Base class for agents that can learn from experience.
    
    Extends BaseAgent with learning capabilities.
    """
    
    def __init__(self, name: str, learning_rate: float = 0.1):
        """
        Initialize the learning agent.
        
        Args:
            name: A unique identifier for the agent
            learning_rate: Rate at which the agent learns (0.0 to 1.0)
        """
        super().__init__(name)
        self.learning_rate = learning_rate
        self.experience: List[Dict[str, Any]] = []
    
    @abstractmethod
    def learn(self, reward: float) -> None:
        """
        Learn from the result of an action.
        
        Args:
            reward: Feedback signal indicating success/failure
        """
        pass
    
    def run_cycle_with_feedback(
        self, 
        observation: Observation, 
        reward: Optional[float] = None
    ) -> Optional[Any]:
        """
        Execute a cycle with learning feedback.
        
        Args:
            observation: The current observation
            reward: Optional feedback from previous action
            
        Returns:
            The result of the action, if any
        """
        # Perceive first to update current state
        self.state = AgentState.THINKING
        self.perceive(observation)
        
        # Learn from previous action if feedback provided
        if reward is not None:
            self.state = AgentState.LEARNING
            self.learn(reward)
        
        # Make decision and act
        action = self.decide()
        
        if action:
            self.state = AgentState.ACTING
            result = self.act(action)
            self.actions_taken.append(action)
            self.state = AgentState.IDLE
            return result
        
        self.state = AgentState.IDLE
        return None
