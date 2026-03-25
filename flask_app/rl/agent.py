import numpy as np
import random
from collections import deque

# --- try to import torch, fall back gracefully ---
try:
    import torch
    import torch.nn as nn
    import torch.optim as optim
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False


# ── Q-Network ────────────────────────────────────────────────────────────────

class QNetwork(nn.Module):
    def __init__(self, state_size, action_size):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(state_size, 64),
            nn.ReLU(),
            nn.Linear(64, 64),
            nn.ReLU(),
            nn.Linear(64, action_size),
        )

    def forward(self, x):
        return self.net(x)


# ── Replay Buffer ─────────────────────────────────────────────────────────────

class ReplayBuffer:
    def __init__(self, capacity=10000):
        self.buffer = deque(maxlen=capacity)

    def push(self, state, action, reward, next_state, done):
        self.buffer.append((state, action, reward, next_state, done))

    def sample(self, batch_size):
        batch = random.sample(self.buffer, batch_size)
        states, actions, rewards, next_states, dones = zip(*batch)
        return (np.array(states), np.array(actions), np.array(rewards, dtype=np.float32),
                np.array(next_states), np.array(dones, dtype=np.float32))

    def __len__(self):
        return len(self.buffer)


# ── DQN Agent ─────────────────────────────────────────────────────────────────

class DQNAgent:
    """
    Deep Q-Network agent for the Landslide Simulator.

    Hyperparameters (all tunable):
        gamma       — discount factor (how much future rewards matter)
        lr          — learning rate
        epsilon     — starting exploration rate (1.0 = fully random)
        epsilon_min — minimum exploration rate
        epsilon_decay — how fast exploration reduces each episode
        batch_size  — how many experiences to learn from at once
        update_target_every — how often to sync target network
    """

    def __init__(self, state_size, action_size,
                 gamma=0.95, lr=1e-3,
                 epsilon=1.0, epsilon_min=0.05, epsilon_decay=0.995,
                 batch_size=64, update_target_every=10):

        assert TORCH_AVAILABLE, "PyTorch is required. Run: pip install torch"

        self.state_size   = state_size
        self.action_size  = action_size
        self.gamma        = gamma
        self.epsilon      = epsilon
        self.epsilon_min  = epsilon_min
        self.epsilon_decay= epsilon_decay
        self.batch_size   = batch_size
        self.update_target_every = update_target_every
        self.steps        = 0

        self.memory = ReplayBuffer()

        self.policy_net = QNetwork(state_size, action_size)
        self.target_net = QNetwork(state_size, action_size)
        self.target_net.load_state_dict(self.policy_net.state_dict())
        self.target_net.eval()

        self.optimizer = optim.Adam(self.policy_net.parameters(), lr=lr)
        self.loss_fn   = nn.MSELoss()

    def act(self, state, greedy=False):
        """Pick an action. Greedy=True means no exploration (use at test time)."""
        if not greedy and random.random() < self.epsilon:
            return random.randrange(self.action_size)
        state_t = torch.FloatTensor(state).unsqueeze(0)
        with torch.no_grad():
            q_values = self.policy_net(state_t)
        return q_values.argmax().item()

    def remember(self, state, action, reward, next_state, done):
        self.memory.push(state, action, reward, next_state, done)

    def learn(self):
        if len(self.memory) < self.batch_size:
            return None

        states, actions, rewards, next_states, dones = self.memory.sample(self.batch_size)

        states_t      = torch.FloatTensor(states)
        actions_t     = torch.LongTensor(actions).unsqueeze(1)
        rewards_t     = torch.FloatTensor(rewards)
        next_states_t = torch.FloatTensor(next_states)
        dones_t       = torch.FloatTensor(dones)

        # current Q values
        current_q = self.policy_net(states_t).gather(1, actions_t).squeeze(1)

        # target Q values (Bellman equation)
        with torch.no_grad():
            max_next_q = self.target_net(next_states_t).max(1)[0]
            target_q   = rewards_t + self.gamma * max_next_q * (1 - dones_t)

        loss = self.loss_fn(current_q, target_q)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        # decay exploration
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)

        # sync target network periodically
        self.steps += 1
        if self.steps % self.update_target_every == 0:
            self.target_net.load_state_dict(self.policy_net.state_dict())

        return loss.item()

    def save(self, path):
        torch.save({
            'policy_net': self.policy_net.state_dict(),
            'epsilon':    self.epsilon,
        }, path)
        print(f"Agent saved to {path}")

    def load(self, path):
        checkpoint = torch.load(path, map_location='cpu')
        self.policy_net.load_state_dict(checkpoint['policy_net'])
        self.target_net.load_state_dict(checkpoint['policy_net'])
        self.epsilon = checkpoint.get('epsilon', self.epsilon_min)
        print(f"Agent loaded from {path}")
