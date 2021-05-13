from AI2048 import config
from AI2048.game import GameState


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

    def run(self, game_display):
        ''' Plays the game based on configuration file '''
        abstract


class ManualTextAgent(Agent):
    ''' Agent for play from text input '''
    def __init__(self):
        super(ManualTextAgent, self).__init__()
        self.name = 'ManualTextAgent'
        self.config = self.get_config()
        self.move_dict = {'r': 'right', 'l': 'left', 'u': 'up', 'd': 'down'}

    def run(self, game_display):
        game = GameState(size=self.config['size'])
        game_display.show(game)
        while not game.lost:
            move = input('Enter a move (l, r, u, d): ')
            if not move in self.move_dict.keys():
                break
            game.move(self.move_dict[move])
            game_display.show(game)
