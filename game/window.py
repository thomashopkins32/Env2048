'''
Contributor(s): Thomas Hopkins

Object module for Application class
'''

import tkinter as tk
import tkinter.messagebox as messagebox
import time

import game.constants as c
from game.game import GameState

class Application(tk.Frame):
    '''
    Class for visualizing game results
    '''
    def __init__(self, master=None, option='manual'):
        '''
        Builds window and launches simulation
        '''
        super().__init__(master)
        self.master = master
        self.init_window()
        self.score_raw = 0
        if option == 'genetic':
            pass
        elif option == 'manual':
            self.master.bind('<Key>', self.key_pressed)
            self.game_state = GameState()
            self.update_labels(self.game_state.get_board())
        elif option == 'expectimax':
            pass

    def init_window(self):
        '''
        Fills the window wiht content
        '''
        self.master.geometry(c.GEOMETRY)
        self.master.title('2048')
        self.header = tk.Frame(self.master, bg='#92877d')
        self.create_header_widgets(self.header)

        self.content = tk.Frame(self.master, bg='#92877d')
        self.create_content_grid(self.content)

        layout = [[self.header], [self.content]]
        col_weights = [1]
        row_weights = [1, 99]
        self.create_grid(self.master, layout, row_weights, col_weights)

    def create_grid(self, container, layout, r_weights, c_weights):
        '''
        Creates a tkinter grid layout with given parameters
        '''
        for i in range(len(layout[0])):
            container.columnconfigure(i, weight=c_weights[i])
        for i in range(len(layout)):
            container.rowconfigure(i, weight=r_weights[i])
        for i in range(len(layout)):
            for j in range(len(layout[i])):
                layout[i][j].grid(row=i, column=j, sticky='nsew')

    def create_header_widgets(self, header):
        '''
        Creates header for displaying score and generation
        '''
        self.score = tk.Label(header, 
            text='Score: ', 
            anchor='w', 
            font=('Helvetica', 18), 
            bg='#92877d')
        self.score.pack()

    def create_content_grid(self, content):
        '''
        Creates grid for the main game
        '''
        self.labels = []
        for i in range(4):
            tmp = []
            for j in range(4):
                tmp.append(tk.Label(content, 
                    bg='#92877d', 
                    text='', 
                    font=('Helvetica', 24), 
                    borderwidth=2, 
                    relief='raised' ))
            self.labels.append(tmp)
        col_weights = [25, 25, 25, 25]
        row_weights = [25, 25, 25 ,25]
        self.create_grid(content, self.labels, row_weights, col_weights)

    def update_labels(self, matrix):
        '''
        Updates window labels
        '''
        for i in range(4):
            for j in range(4):
                new_value = matrix[i][j]
                if new_value == 0:
                    self.labels[i][j].configure(text='', bg='#9e948a')
                else:
                    self.labels[i][j].configure(text=str(new_value), 
                        bg=c.COLORS[new_value])
        score_text = 'Score: ' + str(self.score_raw)
        self.score.configure(text=score_text)
        self.update_idletasks()

    def simulate_game(self, actions, starting_board=[]):
        '''
        Simulates the display of a string of actions
        '''
        game_state = GameState(state=starting_board)
        self.update_labels(game_state.matrix)
        for action in actions:
            game_state.perform_action(action)
            self.update_labels(game_state.matrix)
            if game_state.lost:
                print('simulated game lost :(')
                self.master.destroy()
                quit()
            time.sleep(0.1)
        time.sleep(5)
        self.master.destroy()

    def key_pressed(self, event):
        '''
        Updates the display based on the key pressed by the user
        '''
        e = event.keysym
        self.game_state.perform_action(e)
        self.update_labels(self.game_state.matrix)
        if self.game_state.lost:
            msg_box = messagebox.askyesno(title='You Lost!', message='Do you want to play a new game?')
            if msg_box:
                self.game_state = GameState()
                self.update_labels(self.game_state.matrix)
            else:
                self.master.destroy()
