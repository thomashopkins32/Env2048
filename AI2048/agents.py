from abc import abstractmethod
import time

import matplotlib.pyplot as plt
import numpy as np
import torch
import torch.optim as optim
import torch.nn.functional as F
from tqdm import tqdm

from AI2048 import config
from AI2048.game import Env2048
from AI2048.model import DQN, ReplayMemory, Transition


class Agent:
    ''' Abstract class for agent '''
    def __init__(self):
        self.name = 'Agent'

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    def get_config(self):
        return config.read(f'./config/{self.name}.yml')

    @abstractmethod
    def run(self, game_display):
        ''' Plays/learns the game based on configuration file and updates given display '''
        pass


class ManualTextAgent(Agent):
    ''' Agent for play from text input '''
    def __init__(self):
        super(ManualTextAgent, self).__init__()
        self.name = 'ManualTextAgent'
        self.config = self.get_config()

    def run(self, game_display):
        game = Env2048(size=self.config['size'])
        game_display.show(game)
        while not game._episode_ended:
            action = int(input('Enter a move (0,1,2,3): '))
            if action < 0 or action > 3:
                break
            game._step(action)
            game_display.show(game)


class KeyboardAgent(Agent):
    ''' Agents for play from keyboard input '''
    def __init__(self):
        super(KeyboardAgent, self).__init__()
        self.name = 'KeyboardAgent'
        self.config = self.get_config()

    def run(self, game_display):
        game = Env2048(size=self.config['size'])
        # give game to display (needed to get key presses)
        game_display.run(game)


class RandomAgent(Agent):
    ''' Agent that chooses actions randomly '''
    def __init__(self):
        super(RandomAgent, self).__init__()
        self.name = 'RandomAgent'
        self.config = self.get_config()

    def run(self, game_display):
        game = Env2048(size=self.config['size'])
        game_display.show(game)
        while not game._episode_ended:
            action = np.random.randint(0, 4)
            game._step(action)
            game_display.show(game)


class DQNAgent(Agent):
    ''' Agent that learns using deep-Q networks '''
    def __init__(self):
        super(DQNAgent, self).__init__()
        self.name = 'DQNAgent'
        self.config = self.get_config()
        self.model = None
        self.target = None
        self.optimizer = None
        self.memory = None

    def run(self, game_display):
        self.device = self.config['device']
        ckpt_path = self.config['ckpt_path']
        training = self.config['train']
        self.model = DQN(self.config['size']).to(self.device)


        if training:
            self.optimizer = optim.RMSprop(self.model.parameters(),
                                           lr=self.config['learning_rate'])
            self.target = DQN(self.config['size']).to(self.device)
            if ckpt_path is not None:
                checkpoint = torch.load(ckpt_path)
                self.model.load_state_dict(checkpoint['model_state_dict'])
                self.optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
            self.target.load_state_dict(self.model.state_dict())
            self.target.eval()
            self.train(game_display)
        else:
            if ckpt_path is not None:
                checkpoint = torch.load(ckpt_path)
                self.model.load_state_dict(checkpoint['model_state_dict'])
            self.model.eval()
            self.eval(game_display)

    def optimize(self):
        batch_size = self.config['batch_size']
        gamma = self.config['discount']
        if len(self.memory) < batch_size:
            return
        transitions = self.memory.sample(batch_size)
        batch = Transition(*zip(*transitions))
        non_final_mask = torch.tensor(tuple(map(lambda s: s is not None, batch.next_state)),
                                      device=self.device, dtype=torch.bool)
        non_final_next_states = torch.cat([s for s in batch.next_state if s is not None])
        state_batch = torch.cat(batch.state)
        action_batch = torch.cat(batch.action)
        reward_batch = torch.cat(batch.reward)
        preds = self.model(state_batch)
        state_action_values = preds.gather(1, action_batch)
        next_state_values = torch.zeros(batch_size, device=self.device)
        # double DQN
        next_preds = self.model(non_final_next_states)
        targets = self.target(non_final_next_states)
        next_actions = next_preds.argmax(dim=1).unsqueeze(1)
        next_state_values[non_final_mask] = targets.gather(1, next_actions).squeeze()
        expected_state_action_values = (next_state_values*gamma) + reward_batch

        loss = F.smooth_l1_loss(state_action_values, expected_state_action_values.unsqueeze(1))
        self.losses.append(loss.item())
        self.optimizer.zero_grad()
        loss.backward()
        for param in self.model.parameters():
            param.grad.data.clamp_(-1, 1)
        self.optimizer.step()

    def select_eps_greedy(self, state):
        sample = np.random.random()
        eps_end = self.config['eps_end']
        eps_start = self.config['eps_start']
        eps_decay = self.config['eps_decay']
        eps_threshold = eps_end + (eps_start - eps_end) * \
            np.exp(-1. * self.episode / eps_decay)
        if sample > eps_threshold:
            with torch.no_grad():
                action = torch.argmax(self.model(state)).view(1, 1)
                return action
        else:
            return torch.tensor([[np.random.randint(0, 4)]],
                                device=self.device,
                                dtype=torch.long)

    def train(self, game_display):
        size = self.config['size']
        batch_size = self.config['batch_size']
        target_update = self.config['target_update']
        num_episodes = self.config['num_episodes']
        memory_size = self.config['memory_size']
        self.memory = ReplayMemory(memory_size)
        self.episode = 0
        self.losses = []
        self.rewards = []
        self.durations = []

        for self.episode in tqdm(range(num_episodes), total=num_episodes):
            game = Env2048(size)
            state = torch.tensor([game._state], dtype=torch.float,
                                 device=self.device)
            next_state = None
            duration = 0
            accumulated_reward = 0
            while not game._episode_ended:
                action = self.select_eps_greedy(state)
                transition = game._step(action.item())
                done = game._episode_ended
                if not done:
                    next_state = torch.tensor([game._state], dtype=torch.float,
                                              device=self.device)
                else:
                    next_state = None
                reward = float(transition.reward)
                if not done and torch.equal(state, next_state):
                     reward = -1.0
                accumulated_reward += reward
                reward = torch.tensor([reward], device=self.device)

                self.memory.push(state, action, next_state, reward)

                state = next_state

                self.optimize()

                duration += 1
                if done:
                    self.durations.append(duration)
                    self.rewards.append(accumulated_reward)
                    break
            if self.episode % target_update == 0:
                self.target.load_state_dict(self.model.state_dict())
        print('Done Training')
        torch.save({'model_state_dict': self.model.state_dict(),
                    'optimizer_state_dict': self.optimizer.state_dict() },
                   './models/DQN.pt')
        print('Model Saved')
        fig, (ax1, ax2, ax3) = plt.subplots(1, 3)
        ax1.plot(range(len(self.rewards)), self.rewards)
        ax1.set_title('Cumulative reward per episode')
        ax1.set_ylabel('Cumulative reward')
        ax1.set_xlabel('Episode')
        ax2.plot(range(len(self.durations)), self.durations)
        ax2.set_title('Game duration per episode')
        ax2.set_ylabel('Duration (# of game steps)')
        ax2.set_xlabel('Episode')
        ax3.plot(range(len(self.losses)), self.losses)
        ax3.set_title('Loss per optimization step')
        ax3.set_ylabel('Loss')
        ax3.set_xlabel('Optimization Step')
        plt.show()

        self.model.eval()
        self.eval(game_display)

    def eval(self, game_display):
        game = Env2048(size=self.config['size'])
        game_display.show(game)
        while not game._episode_ended:
            state = torch.tensor(game._state, dtype=torch.float).to(self.device)
            action_vals = self.model(state)
            action = torch.argmax(action_vals).item()
            transition = game._step(action)
            game_display.show(game)
            time.sleep(0.25)
