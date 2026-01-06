"""
Tests for the core agent framework.
"""

import pytest
import time
from src.core import BaseAgent, LearningAgent, Observation, Action, AgentState


class TestAgent(BaseAgent):
    """Concrete implementation of BaseAgent for testing."""
    
    def __init__(self, name: str):
        super().__init__(name)
        self.perceived_data = []
        self.decision_made = False
        
    def perceive(self, observation: Observation) -> None:
        self.perceived_data.append(observation.data)
        self.observations.append(observation)
        
    def decide(self) -> Action:
        self.decision_made = True
        return Action(name="test_action", parameters={"test": True})
        
    def act(self, action: Action) -> str:
        return f"Executed {action.name}"


class TestLearningAgentImpl(LearningAgent):
    """Concrete implementation of LearningAgent for testing."""
    
    def __init__(self, name: str):
        super().__init__(name)
        self.learned_rewards = []
        
    def perceive(self, observation: Observation) -> None:
        self.observations.append(observation)
        
    def decide(self) -> Action:
        return Action(name="learn_action", parameters={})
        
    def act(self, action: Action) -> str:
        return "Learning action executed"
        
    def learn(self, reward: float) -> None:
        self.learned_rewards.append(reward)


class TestBaseAgent:
    """Test cases for BaseAgent."""
    
    def test_agent_initialization(self):
        """Test agent is properly initialized."""
        agent = TestAgent("TestBot")
        assert agent.name == "TestBot"
        assert agent.state == AgentState.IDLE
        assert len(agent.observations) == 0
        assert len(agent.actions_taken) == 0
    
    def test_perceive(self):
        """Test perception of observations."""
        agent = TestAgent("TestBot")
        obs = Observation(data={"sensor": "value"}, timestamp=time.time())
        
        agent.perceive(obs)
        
        assert len(agent.perceived_data) == 1
        assert agent.perceived_data[0] == {"sensor": "value"}
    
    def test_decide(self):
        """Test decision making."""
        agent = TestAgent("TestBot")
        action = agent.decide()
        
        assert agent.decision_made
        assert action.name == "test_action"
        assert action.parameters == {"test": True}
    
    def test_act(self):
        """Test action execution."""
        agent = TestAgent("TestBot")
        action = Action(name="test", parameters={})
        
        result = agent.act(action)
        
        assert result == "Executed test"
    
    def test_run_cycle(self):
        """Test complete perception-decision-action cycle."""
        agent = TestAgent("TestBot")
        obs = Observation(data={"test": "data"}, timestamp=time.time())
        
        result = agent.run_cycle(obs)
        
        assert len(agent.observations) == 1
        assert len(agent.actions_taken) == 1
        assert agent.state == AgentState.IDLE
        assert result == "Executed test_action"
    
    def test_reset(self):
        """Test agent reset functionality."""
        agent = TestAgent("TestBot")
        obs = Observation(data={"test": "data"}, timestamp=time.time())
        
        agent.run_cycle(obs)
        agent.reset()
        
        assert agent.state == AgentState.IDLE
        assert len(agent.observations) == 0
        assert len(agent.actions_taken) == 0


class TestObservation:
    """Test cases for Observation dataclass."""
    
    def test_observation_creation(self):
        """Test observation can be created with required fields."""
        obs = Observation(data="test", timestamp=123.45)
        
        assert obs.data == "test"
        assert obs.timestamp == 123.45
        assert obs.metadata is None
    
    def test_observation_with_metadata(self):
        """Test observation with optional metadata."""
        obs = Observation(
            data="test",
            timestamp=123.45,
            metadata={"source": "sensor1"}
        )
        
        assert obs.metadata == {"source": "sensor1"}


class TestAction:
    """Test cases for Action dataclass."""
    
    def test_action_creation(self):
        """Test action can be created with required fields."""
        action = Action(name="move", parameters={"direction": "north"})
        
        assert action.name == "move"
        assert action.parameters == {"direction": "north"}
        assert action.confidence == 1.0
    
    def test_action_with_confidence(self):
        """Test action with custom confidence value."""
        action = Action(
            name="move",
            parameters={"direction": "north"},
            confidence=0.8
        )
        
        assert action.confidence == 0.8


class TestLearningAgent:
    """Test cases for LearningAgent."""
    
    def test_learning_agent_initialization(self):
        """Test learning agent is properly initialized."""
        agent = TestLearningAgentImpl("LearningBot")
        
        assert agent.name == "LearningBot"
        assert agent.learning_rate == 0.1
        assert len(agent.experience) == 0
    
    def test_learning_agent_custom_learning_rate(self):
        """Test learning agent with custom learning rate."""
        agent = TestLearningAgentImpl("LearningBot")
        agent.learning_rate = 0.5
        
        assert agent.learning_rate == 0.5
    
    def test_learn(self):
        """Test learning from feedback."""
        agent = TestLearningAgentImpl("LearningBot")
        
        agent.learn(10.0)
        agent.learn(-5.0)
        
        assert len(agent.learned_rewards) == 2
        assert agent.learned_rewards == [10.0, -5.0]
    
    def test_run_cycle_with_feedback(self):
        """Test cycle with learning feedback."""
        agent = TestLearningAgentImpl("LearningBot")
        obs = Observation(data="test", timestamp=time.time())
        
        result = agent.run_cycle_with_feedback(obs, reward=5.0)
        
        assert len(agent.learned_rewards) == 1
        assert agent.learned_rewards[0] == 5.0
        assert result == "Learning action executed"
    
    def test_run_cycle_without_feedback(self):
        """Test cycle without learning feedback."""
        agent = TestLearningAgentImpl("LearningBot")
        obs = Observation(data="test", timestamp=time.time())
        
        result = agent.run_cycle_with_feedback(obs)
        
        assert len(agent.learned_rewards) == 0
        assert result == "Learning action executed"


class TestAgentState:
    """Test cases for AgentState enum."""
    
    def test_agent_states(self):
        """Test all agent states exist."""
        assert AgentState.IDLE.value == "idle"
        assert AgentState.THINKING.value == "thinking"
        assert AgentState.ACTING.value == "acting"
        assert AgentState.LEARNING.value == "learning"
        assert AgentState.STOPPED.value == "stopped"
