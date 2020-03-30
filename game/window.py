'''
Contributor(s): Thomas Hopkins

Object module for Application class
'''

import tkinter as tk
import constants as c
import logic

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
        self.matrix = logic.new_game()
        self.matrix = logic.add_new(self.matrix)
        self.matrix = logic.add_new(self.matrix)
        self.update_labels()
        if option == 'genetic':
            self.simulate()
        elif option == 'manual':
            self.master.bind('<Key>', self.key_pressed)
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
        self.create_grid(self.master, layout=layout, r_weights=row_weights, c_weights=col_weights)

    def create_grid(self, container, layout=[], r_weights=[], c_weights=[]):
        '''
        Creates a tkinter grid layout with given parameters
        '''
        if layout == [] or r_weights == [] or c_weights == []:
            print('Error creating grid with empty layout...')
            quit()
        for i in range(len(layout[0])):
            container.columnconfigure(i, weight=c_weights[i])
        for i in range(len(layout)):
            container.rowconfigure(i, weight=r_weights[i])
        for i in range(len(layout)):
            for j in range(len(layout[i])):
                layout[i][j].grid(row=i, column=j, sticky='nsew')

    def simulate(self):
        '''
        AI main loop
        '''
        pass

    def create_header_widgets(self, header):
        '''
        Creates header for displaying score and generation
        '''
        self.score = tk.Label(header, text='Score: ', anchor='w', font=('Helvetica', 18), bg='#92877d')
        self.gen = tk.Label(header, text='Generation: ', anchor='w', font=('Helvetica', 18), bg='#92877d')
        self.score.pack()
        self.gen.pack()

    def create_content_grid(self, content):
        '''
        Creates grid for the main game
        '''
        self.labels = []
        for i in range(4):
            tmp = []
            for j in range(4):
                tmp.append(tk.Label(content, bg='#92877d', text='', font=('Helvetica', 24), borderwidth=2, relief='raised' ))
            self.labels.append(tmp)
        col_weights = [25, 25, 25, 25]
        row_weights = [25, 25, 25 ,25]
        self.create_grid(content, layout=self.labels, r_weights=row_weights, c_weights=col_weights)

    def update_labels(self):
        '''
        Updates window labels
        '''
        for i in range(4):
            for j in range(4):
                new_value = self.matrix[i][j]
                if new_value == 0:
                    self.labels[i][j].configure(text='', bg='#9e948a')
                else:
                    self.labels[i][j].configure(text=str(new_value), bg=c.COLORS[new_value])
        score_text = 'Score: ' + str(self.score_raw)
        self.score.configure(text=score_text)
        self.update_idletasks()

    def update_gen(self, gen):
        '''
        Updates generation widget
        '''
        gen_text = 'Generation: ' + str(gen)
        self.gen.configure(text=gen_text)
        self.update_idletasks()

    def key_pressed(self, event):
        e = event.keysym
        if e == 'Right':
            self.matrix = logic.right(self.matrix)
        elif e == 'Left':
            self.matrix = logic.left(self.matrix)
        elif e == 'Up':
            self.matrix = logic.up(self.matrix)
        elif e == 'Down':
            self.matrix = logic.down(self.matrix)
        self.matrix = logic.add_new(self.matrix)
        self.update_labels()
        game_state = logic.game_state(self.matrix)
        if game_state == 'win':
            print('You Win!')
            self.master.destroy()
        elif game_state == 'lose':
            print('You Lose!')
            self.master.destroy()
