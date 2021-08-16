from abc import abstractmethod

import numpy as np

from AI2048 import config
from AI2048.game import Env2048


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
