from collections import namedtuple
import random

import torch
import torch.nn as nn
import torch.nn.functional as F


Transition = namedtuple('Transition',
                        ('state', 'action', 'next_state', 'reward'))


class ReplayMemory:
    '''
    Memory for (s, a, s', r) transitions.
    '''
    def __init__(self, capacity):
        self.capacity = capacity
        self.memory = []
        self.position = 0

    def push(self, *args):
        ''' Saves a transition '''
        if len(self.memory) < self.capacity:
            self.memory.append(None)
        self.memory[self.position] = Transition(*args)
        self.position = (self.position + 1) % self.capacity

    def sample(self, batch_size):
        ''' Uniformly sample a batch of transitions '''
        return random.sample(self.memory, batch_size)

    def __len__(self):
        return len(self.memory)


class DQN(nn.Module):
    ''' Deep-Q Network architecture '''
    def __init__(self, game_size):
        super(DQN, self).__init__()
        self.size = game_size
        self.l1 = nn.Linear(self.size*self.size, 16)
        self.l2 = nn.Linear(16, 8)
        self.l3 = nn.Linear(8, 4)

    def forward(self, state):
        x = state.reshape(-1, self.size*self.size)
        x = F.relu(self.l1(x))
        x = F.relu(self.l2(x))
        return self.l3(x)
