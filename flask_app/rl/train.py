"""
Train the DQN agent on the Landslide Simulator environment.

Usage:
    python train.py              # train with defaults
    python train.py --episodes 2000
"""

import sys, os, argparse
sys.path.insert(0, os.path.dirname(__file__))

import numpy as np
from landslide_env import LandslideEnv
from agent import DQNAgent

def train(episodes=1000, save_path='trained_agent.pt', print_every=100):
    env   = LandslideEnv()
    agent = DQNAgent(state_size=env.STATE_SIZE, action_size=env.N_ACTIONS)

    best_reward = -float('inf')
    reward_history = []

    for ep in range(1, episodes + 1):
        state = env.reset()
        total_reward = 0.0

        while True:
            action = agent.act(state)
            next_state, reward, done = env.step(action)

            # normalize reward to keep gradients stable
            agent.remember(state, action, reward / 10000.0, next_state, done)
            agent.learn()

            state = next_state
            total_reward += reward

            if done:
                break

        reward_history.append(total_reward)

        # save best model
        if total_reward > best_reward:
            best_reward = total_reward
            agent.save(save_path)

        if ep % print_every == 0:
            avg = np.mean(reward_history[-print_every:])
            print(f"Episode {ep:4d} | Avg Reward (last {print_every}): {avg:>12.1f} "
                  f"| Best: {best_reward:>12.1f} | Epsilon: {agent.epsilon:.3f}")

    print("\nTraining complete.")
    print(f"Best final wealth achieved: {best_reward:.1f}")
    return agent, reward_history


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--episodes',   type=int, default=1000)
    parser.add_argument('--save_path',  type=str, default='trained_agent.pt')
    parser.add_argument('--print_every',type=int, default=100)
    args = parser.parse_args()

    train(episodes=args.episodes, save_path=args.save_path, print_every=args.print_every)
