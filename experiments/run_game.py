import sys

from env2048.env import Env2048
import torch.nn as nn
import torch
from torch.distributions.categorical import Categorical

class MLP(nn.Module):
    def __init__(self, nodes_per_layer, activation='relu'):
        '''
        A basic multi-layered perceptron using PyTorch.
        Parameters
        ----------
        nodes_per_layer : List[int]
            number of nodes per layer in the network
        activation : str, optional
            description of activation to use in between layers
            supports: {'sigmoid', 'relu', 'tanh'}
        '''
        super().__init__()
        activ_func = None
        if activation == 'relu':
            activ_func = nn.ReLU()
        elif activation == 'sigmoid':
            activ_func = nn.Sigmoid()
        elif activation == 'tanh':
            activ_func = nn.Tanh()
        self.mlp = nn.Sequential()
        # game state is 2D tensor but we need 1D tensor
        nodes_per_layer[0] = nodes_per_layer[0] ** 2
        # add layers
        for i in range(1, len(nodes_per_layer)):
            self.mlp.append(nn.Linear(nodes_per_layer[i-1],
                                    nodes_per_layer[i]))
            if activ_func is not None and i != len(nodes_per_layer)-1:
                self.mlp.append(activ_func)

    def forward(self, x):
        if len(x.shape) == 3:
            x = torch.flatten(x, start_dim=1)
        else:
            x = torch.flatten(x)
        return self.mlp(x)


class ActorCriticMLP:
    ''' Actor/Critic that performs actions and makes value estimates '''
    def __init__(self, obs_dim, act_dim):
        self.actor = MLP([obs_dim, 256, 128, act_dim], activation='tanh')
        self.critic = MLP([obs_dim, 256, 128, 1], activation='tanh')

    def distribution(self, obs, mask=None):
        ''' Returns the current policy distribution over the observation '''
        logits = self.actor(obs)
        print(f'before: {logits}')
        if mask is not None:
            logits = logits.masked_fill((1 - mask), float('-inf'))
        print(f'after {logits}')
        return Categorical(logits=logits)

    def policy(self, obs, act=None, mask=None):
        ''' Returns an action given the observation '''
        pi = self.distribution(obs, mask=mask)
        logp_a = None
        if act is not None:
            logp_a = pi.log_prob(act)
        return pi, logp_a

    def value(self, obs):
        ''' Returns the perceived value of the observation '''
        return self.critic(obs)

    def step(self, obs, mask=None):
        ''' Returns the action, value, and logp_a for the observation '''
        pi, _ = self.policy(obs, mask=mask)
        a = pi.sample()
        logp = pi.log_prob(a)
        v = self.value(obs)
        return a.item(), v.item(), logp.item(), pi
    
    
env = Env2048()
ac = ActorCriticMLP(env.observation_space.shape[0],
                    env.action_space.n)
checkpoint = torch.load(f'{sys.argv[1]}_model.pt')
ac.actor.load_state_dict(checkpoint['actor'])
ac.critic.load_state_dict(checkpoint['critic'])

done = False
o = env.reset()
env.render()
mask = torch.ones((4,), dtype=int)
while not done:
    with torch.no_grad():
        a, v, logp, pi = ac.step(torch.as_tensor(o, dtype=torch.float32),
                             mask=mask)
    print(pi.probs)
    o, _, done, info = env.step(a)
    print('-----------------------------------------')
    print(o, a, v, logp, info)
    mask = torch.as_tensor(info['action_mask'])
    env.render()