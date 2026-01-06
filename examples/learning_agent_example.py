"""
Q-Learning Agent Example

This example demonstrates a learning agent that learns to navigate a simple grid world.
"""

import time
import random
from src.core import Observation
from src.agents.qlearning_agent import QLearningAgent


class GridWorld:
    """A simple 3x3 grid world environment."""
    
    def __init__(self):
        self.size = 3
        self.agent_pos = [0, 0]  # Start at top-left
        self.goal_pos = [2, 2]   # Goal at bottom-right
        self.steps = 0
        self.max_steps = 50
    
    def reset(self):
        """Reset the environment."""
        self.agent_pos = [0, 0]
        self.steps = 0
    
    def get_state(self):
        """Get current state as string."""
        return f"{self.agent_pos[0]},{self.agent_pos[1]}"
    
    def step(self, action: str):
        """
        Execute an action and return reward.
        
        Args:
            action: One of 'up', 'down', 'left', 'right'
            
        Returns:
            reward: Numerical reward for the action
        """
        self.steps += 1
        
        # Apply action
        new_pos = self.agent_pos.copy()
        if action == 'up':
            new_pos[0] = max(0, new_pos[0] - 1)
        elif action == 'down':
            new_pos[0] = min(self.size - 1, new_pos[0] + 1)
        elif action == 'left':
            new_pos[1] = max(0, new_pos[1] - 1)
        elif action == 'right':
            new_pos[1] = min(self.size - 1, new_pos[1] + 1)
        
        self.agent_pos = new_pos
        
        # Calculate reward
        if self.agent_pos == self.goal_pos:
            return 100.0  # Big reward for reaching goal
        elif self.steps >= self.max_steps:
            return -50.0  # Penalty for taking too long
        else:
            # Small penalty for each step to encourage efficiency
            return -1.0
    
    def is_done(self):
        """Check if episode is complete."""
        return (self.agent_pos == self.goal_pos or 
                self.steps >= self.max_steps)


def main():
    """Run Q-learning agent example."""
    print("=== Q-Learning Agent Example ===\n")
    print("Learning to navigate a 3x3 grid world to reach the goal\n")
    
    # Create environment and agent
    env = GridWorld()
    agent = QLearningAgent(
        name="GridNavigator",
        actions=['up', 'down', 'left', 'right'],
        learning_rate=0.1,
        discount_factor=0.9,
        exploration_rate=0.2
    )
    
    # Training
    num_episodes = 100
    print(f"Training for {num_episodes} episodes...\n")
    
    episode_rewards = []
    successful_episodes = 0
    
    for episode in range(num_episodes):
        env.reset()
        total_reward = 0
        
        while not env.is_done():
            # Get observation
            obs = Observation(
                data={'position': env.get_state()},
                timestamp=time.time()
            )
            
            # Agent perceives and decides
            agent.perceive(obs)
            action = agent.decide()
            
            if action:
                # Execute action in environment
                reward = env.step(action.name)
                total_reward += reward
                
                # Agent learns from reward
                agent.learn(reward)
                
                # Check if reached goal
                if env.agent_pos == env.goal_pos:
                    successful_episodes += 1
                    break
        
        episode_rewards.append(total_reward)
        
        # Print progress every 20 episodes
        if (episode + 1) % 20 == 0:
            avg_reward = sum(episode_rewards[-20:]) / 20
            success_rate = successful_episodes / (episode + 1) * 100
            print(f"Episode {episode + 1}/{num_episodes}")
            print(f"  Avg Reward (last 20): {avg_reward:.2f}")
            print(f"  Success Rate: {success_rate:.1f}%")
            print(f"  Q-Table Size: {len(agent.q_table)}")
            print()
    
    # Final evaluation
    print("\n=== Training Complete ===\n")
    print("Q-Learning Summary:")
    summary = agent.get_q_table_summary()
    for key, value in summary.items():
        print(f"  {key}: {value}")
    
    print(f"\nSuccess Rate: {successful_episodes/num_episodes*100:.1f}%")
    print(f"Average Reward: {sum(episode_rewards)/len(episode_rewards):.2f}")
    
    # Test learned policy
    print("\n=== Testing Learned Policy ===\n")
    print("Running with no exploration (pure exploitation)...\n")
    
    agent.exploration_rate = 0.0  # No exploration
    env.reset()
    path = [env.get_state()]
    
    while not env.is_done() and len(path) < 20:
        obs = Observation(
            data={'position': env.get_state()},
            timestamp=time.time()
        )
        agent.perceive(obs)
        action = agent.decide()
        
        if action:
            env.step(action.name)
            path.append(env.get_state())
            print(f"Position: {env.get_state()} | Action: {action.name}")
    
    if env.agent_pos == env.goal_pos:
        print(f"\n✓ Successfully reached goal in {len(path)-1} steps!")
    else:
        print(f"\n✗ Did not reach goal")


if __name__ == "__main__":
    main()
