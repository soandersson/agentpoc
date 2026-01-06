"""
Tests for the reactive agent implementation.
"""

import pytest
import time
from src.core import Observation, Action
from src.agents.reactive_agent import ReactiveAgent


class TestReactiveAgent:
    """Test cases for ReactiveAgent."""
    
    def test_initialization(self):
        """Test reactive agent initialization."""
        agent = ReactiveAgent("ReactiveBot")
        
        assert agent.name == "ReactiveBot"
        assert len(agent.rules) == 0
        assert agent.default_action is None
        assert agent.current_observation is None
    
    def test_add_rule(self):
        """Test adding condition-action rules."""
        agent = ReactiveAgent("ReactiveBot")
        
        def rule_fn(data):
            return Action(name="test_action", parameters={})
        
        agent.add_rule("condition1", rule_fn)
        
        assert "condition1" in agent.rules
        assert len(agent.rules) == 1
    
    def test_set_default_action(self):
        """Test setting default action."""
        agent = ReactiveAgent("ReactiveBot")
        default = Action(name="default", parameters={})
        
        agent.set_default_action(default)
        
        assert agent.default_action == default
    
    def test_perceive(self):
        """Test perception stores observation."""
        agent = ReactiveAgent("ReactiveBot")
        obs = Observation(data="test", timestamp=time.time())
        
        agent.perceive(obs)
        
        assert agent.current_observation == obs
        assert len(agent.observations) == 1
    
    def test_decide_with_matching_rule_dict(self):
        """Test decision with matching rule for dict data."""
        agent = ReactiveAgent("ReactiveBot")
        
        def hot_rule(data):
            return Action(name="cool", parameters={"temp": data['temp']})
        
        agent.add_rule("hot", hot_rule)
        
        obs = Observation(data={"type": "hot", "temp": 30}, timestamp=time.time())
        agent.perceive(obs)
        
        action = agent.decide()
        
        assert action is not None
        assert action.name == "cool"
        assert action.parameters == {"temp": 30}
    
    def test_decide_with_matching_rule_string(self):
        """Test decision with matching rule for string data."""
        agent = ReactiveAgent("ReactiveBot")
        
        def alert_rule(data):
            return Action(name="respond_alert", parameters={})
        
        agent.add_rule("alert", alert_rule)
        
        obs = Observation(data="alert", timestamp=time.time())
        agent.perceive(obs)
        
        action = agent.decide()
        
        assert action is not None
        assert action.name == "respond_alert"
    
    def test_decide_with_no_matching_rule(self):
        """Test decision returns default when no rules match."""
        agent = ReactiveAgent("ReactiveBot")
        default_action = Action(name="wait", parameters={})
        agent.set_default_action(default_action)
        
        def rule_fn(data):
            return Action(name="other", parameters={})
        
        agent.add_rule("specific", rule_fn)
        
        obs = Observation(data="unknown", timestamp=time.time())
        agent.perceive(obs)
        
        action = agent.decide()
        
        assert action == default_action
    
    def test_decide_no_observation(self):
        """Test decision with no current observation."""
        agent = ReactiveAgent("ReactiveBot")
        default_action = Action(name="idle", parameters={})
        agent.set_default_action(default_action)
        
        action = agent.decide()
        
        assert action == default_action
    
    def test_act(self):
        """Test action execution."""
        agent = ReactiveAgent("ReactiveBot")
        action = Action(name="move", parameters={"direction": "north"})
        
        result = agent.act(action)
        
        assert result['agent'] == "ReactiveBot"
        assert result['action'] == "move"
        assert result['parameters'] == {"direction": "north"}
        assert result['success'] is True
    
    def test_complete_cycle(self):
        """Test complete perception-decision-action cycle."""
        agent = ReactiveAgent("ReactiveBot")
        
        def hot_rule(data):
            return Action(name="cool", parameters={})
        
        agent.add_rule("hot", hot_rule)
        
        obs = Observation(data={"type": "hot"}, timestamp=time.time())
        
        result = agent.run_cycle(obs)
        
        assert result is not None
        assert result['action'] == "cool"
        assert len(agent.observations) == 1
        assert len(agent.actions_taken) == 1
    
    def test_multiple_rules(self):
        """Test agent with multiple rules."""
        agent = ReactiveAgent("ReactiveBot")
        
        def rule1(data):
            return Action(name="action1", parameters={})
        
        def rule2(data):
            return Action(name="action2", parameters={})
        
        def rule3(data):
            return Action(name="action3", parameters={})
        
        agent.add_rule("type1", rule1)
        agent.add_rule("type2", rule2)
        agent.add_rule("type3", rule3)
        
        assert len(agent.rules) == 3
        
        # Test each rule
        obs1 = Observation(data={"type": "type1"}, timestamp=time.time())
        agent.perceive(obs1)
        action1 = agent.decide()
        assert action1.name == "action1"
        
        obs2 = Observation(data={"type": "type2"}, timestamp=time.time())
        agent.perceive(obs2)
        action2 = agent.decide()
        assert action2.name == "action2"
