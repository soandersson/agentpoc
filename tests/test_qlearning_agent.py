"""
Tests for the Q-learning agent implementation.
"""

import pytest
import time
from src.core import Observation, Action
from src.agents.qlearning_agent import QLearningAgent


class TestQLearningAgent:
    """Test cases for QLearningAgent."""
    
    def test_initialization(self):
        """Test Q-learning agent initialization."""
        agent = QLearningAgent(
            name="QLearner",
            actions=["up", "down", "left", "right"],
            learning_rate=0.1,
            discount_factor=0.9,
            exploration_rate=0.2
        )
        
        assert agent.name == "QLearner"
        assert agent.available_actions == ["up", "down", "left", "right"]
        assert agent.learning_rate == 0.1
        assert agent.discount_factor == 0.9
        assert agent.exploration_rate == 0.2
        assert len(agent.q_table) == 0
        assert agent.current_state is None
    
    def test_perceive(self):
        """Test observation updates state."""
        agent = QLearningAgent(
            name="QLearner",
            actions=["a", "b"]
        )
        
        obs = Observation(data={"position": "state1"}, timestamp=time.time())
        agent.perceive(obs)
        
        assert agent.current_state is not None
        assert len(agent.observations) == 1
    
    def test_decide_returns_action(self):
        """Test decision returns a valid action."""
        agent = QLearningAgent(
            name="QLearner",
            actions=["a", "b", "c"]
        )
        
        obs = Observation(data="state1", timestamp=time.time())
        agent.perceive(obs)
        
        action = agent.decide()
        
        assert action is not None
        assert action.name in ["a", "b", "c"]
        assert agent.last_action == action.name
    
    def test_decide_without_state(self):
        """Test decision without current state."""
        agent = QLearningAgent(
            name="QLearner",
            actions=["a", "b"]
        )
        
        action = agent.decide()
        
        assert action is None
    
    def test_act(self):
        """Test action execution returns result."""
        agent = QLearningAgent(
            name="QLearner",
            actions=["a", "b"]
        )
        
        obs = Observation(data="state1", timestamp=time.time())
        agent.perceive(obs)
        
        action = Action(name="a", parameters={})
        result = agent.act(action)
        
        assert result['agent'] == "QLearner"
        assert result['action'] == "a"
        assert 'state' in result
        assert 'q_value' in result
    
    def test_learn_updates_q_table(self):
        """Test learning updates Q-table."""
        agent = QLearningAgent(
            name="QLearner",
            actions=["a", "b"],
            learning_rate=0.5
        )
        
        # First observation and action
        obs1 = Observation(data="state1", timestamp=time.time())
        agent.perceive(obs1)
        action = agent.decide()
        
        # Second observation
        obs2 = Observation(data="state2", timestamp=time.time())
        agent.perceive(obs2)
        
        # Learn with reward
        initial_q_size = len(agent.q_table)
        agent.learn(10.0)
        
        assert len(agent.q_table) > initial_q_size
        assert len(agent.experience) == 1
    
    def test_learn_without_prior_action(self):
        """Test learning without prior action does nothing."""
        agent = QLearningAgent(
            name="QLearner",
            actions=["a", "b"]
        )
        
        agent.learn(5.0)
        
        assert len(agent.experience) == 0
        assert len(agent.q_table) == 0
    
    def test_get_q_table_summary(self):
        """Test Q-table summary generation."""
        agent = QLearningAgent(
            name="QLearner",
            actions=["a", "b"]
        )
        
        summary = agent.get_q_table_summary()
        
        assert 'total_entries' in summary
        assert 'total_experiences' in summary
        assert 'average_q_value' in summary
        assert 'states_visited' in summary
        assert summary['total_entries'] == 0
        assert summary['total_experiences'] == 0
    
    def test_q_value_convergence(self):
        """Test Q-values update over multiple learning iterations."""
        agent = QLearningAgent(
            name="QLearner",
            actions=["a", "b"],
            learning_rate=0.5,
            discount_factor=0.9,
            exploration_rate=0.0  # No exploration for deterministic test
        )
        
        # Simulate consistent reward scenario
        for i in range(5):
            obs = Observation(data=f"state{i}", timestamp=time.time())
            agent.perceive(obs)
            
            if i > 0:
                agent.learn(10.0)
            
            action = agent.decide()
        
        # Should have Q-table entries
        assert len(agent.q_table) > 0
        assert len(agent.experience) == 4  # learned 4 times (skipped first)
    
    def test_state_from_observation_dict(self):
        """Test state extraction from dict observation."""
        agent = QLearningAgent(
            name="QLearner",
            actions=["a"]
        )
        
        obs = Observation(data={"x": 1, "y": 2}, timestamp=time.time())
        agent.perceive(obs)
        
        assert agent.current_state is not None
        assert isinstance(agent.current_state, str)
    
    def test_state_from_observation_string(self):
        """Test state extraction from string observation."""
        agent = QLearningAgent(
            name="QLearner",
            actions=["a"]
        )
        
        obs = Observation(data="simple_state", timestamp=time.time())
        agent.perceive(obs)
        
        assert agent.current_state == "simple_state"
    
    def test_run_cycle_with_feedback(self):
        """Test complete cycle with learning feedback."""
        agent = QLearningAgent(
            name="QLearner",
            actions=["a", "b"]
        )
        
        # First cycle
        obs1 = Observation(data="state1", timestamp=time.time())
        result1 = agent.run_cycle_with_feedback(obs1)
        
        # Second cycle with feedback
        obs2 = Observation(data="state2", timestamp=time.time())
        result2 = agent.run_cycle_with_feedback(obs2, reward=5.0)
        
        assert len(agent.experience) == 1
        assert agent.experience[0]['reward'] == 5.0
