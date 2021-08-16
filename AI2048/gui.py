import tkinter as tk
from tkinter import ttk
from tkinter import N, S, E, W

import importlib

from AI2048 import config


COLOR_DICT = {2: '#d9ed92',
              4: '#b5e48c',
              8: '#99d98c',
              16: '#76c893',
              32: '#52b69a',
              64: '#34a0a4',
              128: '#168aad',
              256: '#1a759f',
              512: '#1e6091',
              1024: '#184e77',
              2048: '#033c57'}

STYLE_DICT = {2: 'T2.TLabel',
              4: 'T4.TLabel',
              8: 'T8.TLabel',
              16: 'T16.TLabel',
              32: 'T32.TLabel',
              64: 'T64.TLabel',
              128: 'T128.TLabel',
              256: 'T256.TLabel',
              512: 'T512.TLabel',
              1024: 'T1024.TLabel',
              2048: 'T2048.TLabel'}


class GameWindow(ttk.Frame):
    '''
    Game window for the 2048 game.
    '''
    def __init__(self, root):
        super(GameWindow, self).__init__(root)
        self.root = root

        # top navigation bar
        self.navbar = NavBar(self)
        self.navbar.grid(column=0, row=0, sticky=(N, S, E, W))

        # frame for board tiles
        self.board = Board(self)
        self.board.grid(column=0, row=1, sticky=(N, S, E, W))

        # expand board twice as much as navbar
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=50)

        self.root.update_idletasks()
        self.game = None # useful for KeyboardAgent

    def _start(self):
        ''' Starts the game/simulation based on agent and configuration '''
        agent_name = self.navbar.selected_agent.get()
        # instantiate the selected agent
        agent_class = getattr(importlib.import_module('AI2048.agents'), agent_name)
        agent = agent_class()
        # pass self so agent can display the board
        board_size = agent.config['size']
        self.board.create_board(board_size)
        self.root.update_idletasks()
        agent.run(self)

    def _key_in(self, event):
        ''' Takes input from the keyboard and manipulates the current game '''
        if self.game is None:
            self.root.quit()
        key_to_action = {'Left': 0, 'Up': 1, 'Right': 2, 'Down': 3}
        if self.game._episode_ended:
            return
        action = key_to_action[event.keysym]
        self.game._step(action)
        self.show(self.game)

    def show(self, game_state):
        ''' Displays the given state in the window '''
        self.board.set_board(game_state._state)
        self.navbar.set_score(game_state.score)
        self.root.update_idletasks()

    def run(self, game):
        ''' Runs a game from keyboard input '''
        self.root.bind('<Key>', self._key_in)
        self.game = game
        self.show(game)


class NavBar(ttk.Frame):
    '''
    Creates a navigation bar which displays the current score,
    options to choose and configure AI agents, and a start button.
    '''
    def __init__(self, root):
        super(NavBar, self).__init__(root)

        self.root = root

        self.score_val = tk.StringVar()
        self.score_label = ttk.Label(self, textvariable=self.score_val, font=('Arial', 16))
        self.score_val.set('Score: 0')
        self.score_label.grid(column=0, row=0, sticky=(N, S, W))

        self.agent_label = ttk.Label(self, text='Agent: ', font=('Arial', 16))
        self.agent_label.grid(column=1, row=0, sticky=(N, S, E))

        self.selected_agent = tk.StringVar()
        self.agent_combo = ttk.Combobox(self, textvariable=self.selected_agent)
        all_agents = config.read('./config/agents.json')
        agents = tuple(all_agents['types'])
        self.agent_combo['values'] = agents
        self.agent_combo.state(['readonly'])
        self.agent_combo.grid(column=2, row=0, sticky=(N, S, E, W))

        self.start_btn = ttk.Button(self, text='Start', command=self.root._start)
        self.start_btn.grid(column=3, row=0, sticky=(N, S, E, W))

        self.columnconfigure(0, weight=2)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.rowconfigure(0, weight=1)

    def set_score(self, score):
        self.score_val.set(f'Score: {score}')


class Board(ttk.Frame):
    ''' Frame for the board and its components '''
    def __init__(self, root):
        super(Board, self).__init__(root)
        self.size = 0
        self.tile_vars = []
        self.tiles = []

    def create_board(self, size):
        self.size = size
        height = self.winfo_height()
        width = self.winfo_width()
        for i in range(size):
            self.tile_vars.append([])
            self.tiles.append([])
            for j in range(size):
                self.tile_vars[i].append(tk.StringVar())
                self.tiles[i].append(ttk.Label(self, textvariable=self.tile_vars[i][j],
                                               font=('Arial', 20), anchor='center'))
                self.tile_vars[i][j].set('')
                self.tiles[i][j].grid(column=j, row=i, sticky=(N, S, E, W))
            self.rowconfigure(i, weight=1, minsize=height // size)
            self.columnconfigure(i, weight=1, minsize=width // size)

    def set_board(self, state):
        for i in range(self.size):
            for j in range(self.size):
                if state[i][j] != 0:
                    self.tile_vars[i][j].set(str(state[i][j]))
                    if state[i][j] > 2048:
                        self.tiles[i][j]['style'] = 'TLarge.TLabel'
                    else:
                        self.tiles[i][j]['style'] = STYLE_DICT[state[i][j]]
                else:
                    self.tile_vars[i][j].set('')
                    self.tiles[i][j]['style'] = 'TLabel'


if __name__ == '__main__':
    root = tk.Tk()
    root.title('2048AI')
    root.geometry('900x900')
    mainframe = GameWindow(root)
    mainframe.grid(column=0, row=0, sticky=(N, S, E, W))
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)
    s = ttk.Style()
    for num, stylename in STYLE_DICT.items():
        s.configure(stylename, background=COLOR_DICT[num])
    s.configure('TLarge.TLabel', background='#033c57')
    root.mainloop()
