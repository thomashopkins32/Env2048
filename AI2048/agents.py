from abc import abstractmethod

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
        return config.read(f'./config/{self.name}.json')

    @abstractmethod
    def run(self, game_display):
        ''' Plays the game based on configuration file '''
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
