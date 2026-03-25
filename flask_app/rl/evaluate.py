"""
Evaluate the trained DQN agent on the Landslide Simulator.

Runs N episodes with no exploration (greedy) and prints:
- Month-by-month decisions
- Final wealth per episode
- Average performance summary

Usage:
    python evaluate.py
    python evaluate.py --episodes 20 --model trained_agent.pt
"""

import sys, os, argparse
sys.path.insert(0, os.path.dirname(__file__))

import numpy as np
from landslide_env import LandslideEnv, DEFAULT_PARAMS
from agent import DQNAgent

ACTION_LABELS = [
    "Do nothing",
    "Invest 10% of income",
    "Invest 20% of income",
    "Invest 30% of income",
    "Buy health insurance only",
    "Buy life insurance only",
    "Buy property insurance only",
    "Buy all 3 insurances",
    "Invest 10% + all insurances",
    "Invest 20% + all insurances",
]


def evaluate(model_path='trained_agent.pt', episodes=10, verbose=True):
    env   = LandslideEnv()
    agent = DQNAgent(state_size=env.STATE_SIZE, action_size=env.N_ACTIONS)
    agent.load(model_path)

    all_final_wealth = []
    all_action_counts = np.zeros(env.N_ACTIONS, dtype=int)

    for ep in range(1, episodes + 1):
        state = env.reset()
        total_reward = 0.0
        episode_log  = []

        while True:
            action = agent.act(state, greedy=True)   # no exploration
            next_state, reward, done = env.step(action)
            total_reward += reward

            episode_log.append({
                'month':        env.day,
                'action':       action,
                'action_label': ACTION_LABELS[action],
                'p_landslide':  round(env.last_p_landslide, 3),
                'damage':       env.last_damage_flag,
                'income':       round(env.daily_income, 1),
                'wealth':       round(env.money_ini, 1),
            })
            all_action_counts[action] += 1
            state = next_state
            if done:
                break

        all_final_wealth.append(env.final_money)

        if verbose:
            print(f"\n{'='*60}")
            print(f"Episode {ep}  |  Final Wealth: {env.final_money:,.1f} EC")
            print(f"{'='*60}")
            print(f"{'Month':<7} {'Action':<38} {'P(slide)':<10} {'Damage':<8} {'Wealth'}")
            print(f"{'-'*80}")
            for log in episode_log:
                dmg = '⚠ YES' if log['damage'] else 'no'
                print(f"{log['month']:<7} {log['action_label']:<38} "
                      f"{log['p_landslide']:<10} {dmg:<8} {log['wealth']:,.1f}")

    # --- summary ---
    print(f"\n{'='*60}")
    print(f"SUMMARY over {episodes} episodes")
    print(f"{'='*60}")
    print(f"  Average final wealth : {np.mean(all_final_wealth):>12,.1f} EC")
    print(f"  Best final wealth    : {np.max(all_final_wealth):>12,.1f} EC")
    print(f"  Worst final wealth   : {np.min(all_final_wealth):>12,.1f} EC")
    print(f"  Std deviation        : {np.std(all_final_wealth):>12,.1f} EC")
    print(f"\n  Action preference (across all episodes):")
    for i, count in enumerate(all_action_counts):
        bar = '█' * (count // max(1, all_action_counts.max() // 20))
        print(f"    [{i}] {ACTION_LABELS[i]:<38} {count:>4}x  {bar}")

    return all_final_wealth


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--model',    type=str, default='trained_agent.pt')
    parser.add_argument('--episodes', type=int, default=10)
    args = parser.parse_args()
    evaluate(model_path=args.model, episodes=args.episodes)
