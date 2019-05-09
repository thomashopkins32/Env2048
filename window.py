from tkinter import Frame, Label, CENTER
import logic as l

BOARD_SIZE = 400
BOARD_LENGTH = 4
BOARD_PADDING = 10
BACKGROUND_COLOR = "#92877d"
EMPTY_CELL_COLOR = "#9e948a"
CELL_COLORS = {2: "#eee4da", 4: "#ede0c8", 8: "#f2b179",
               16: "#f59563", 32: "#f67c5f", 64: "#f65e3b",
               128: "#edcf72", 256: "#edcc61", 512: "#edc850",
               1024: "#edc53f", 2048: "#edc22e"}
FONT = ("Verdana", 40, "bold")
D_KEY_UP = "\'\\uf700\'"
D_KEY_DOWN = "\'\\uf701\'"
D_KEY_LEFT = "\'\\uf702\'"
D_KEY_RIGHT = "\'\\uf703\'"
KEY_UP = "'w'"
KEY_DOWN = "'s'"
KEY_LEFT = "'a'"
KEY_RIGHT = "'d'"

class Window(Frame):
    def __init__(self):
        Frame.__init__(self)

        self.grid()
        self.master.title("2048")
        self.master.bind("<Key>", self.key_down)

        self.commands = { KEY_UP:  l.up, KEY_DOWN:  l.down,
                         KEY_LEFT:  l.left, KEY_RIGHT:  l.right,
                         D_KEY_UP:  l.up, D_KEY_DOWN:  l.down,
                         D_KEY_LEFT:  l.left, D_KEY_RIGHT:  l.right}

        self.grid_cells = []
        self.init_grid()
        self.init_matrix()
        self.update_grid_cells()

        self.mainloop()

    def init_grid(self):
        background = Frame(self, bg=BACKGROUND_COLOR, width=BOARD_SIZE,
                           height=BOARD_SIZE)
        background.grid()

        for i in range(BOARD_LENGTH):
            grid_row = []
            for j in range(BOARD_LENGTH):
                cell = Frame(background, bg=EMPTY_CELL_COLOR,
                             width=BOARD_SIZE/BOARD_LENGTH,
                             height=BOARD_SIZE/BOARD_LENGTH)
                cell.grid(row=i, column=j, padx=BOARD_PADDING, pady=BOARD_PADDING)
                t = Label(master=cell, text="", bg=EMPTY_CELL_COLOR, justify=CENTER,
                          font=FONT, width=5, height=3)
                t.grid()
                grid_row.append(t)

            self.grid_cells.append(grid_row)

    def gen(self):
        return random.randint(0, BOARD_LENGTH - 1)

    def init_matrix(self):
        self.matrix =  l.new_game()
        self.history_matrices = list()
        self.matrix =  l.add_two(self.matrix)
        self.matrix =  l.add_two(self.matrix)

    def update_grid_cells(self):
        for i in range(BOARD_LENGTH):
            for j in range(BOARD_LENGTH):
                num = self.matrix[i][j]
                if num == 0:
                    self.grid_cells[i][j].configure(text="", bg=EMPTY_CELL_COLOR)
                else:
                    self.grid_cells[i][j].configure(text=str(num), bg=CELL_COLORS[num],
                                                    fg=CELL_COLORS[num])
        self.update_idletasks()

    def key_down(self, event):
        key = repr(event.char)
        if key in self.commands:
            self.matrix = self.commands[repr(event.char)](self.matrix)
            done = True
            if done:
                self.matrix =  l.add_two(self.matrix)
                self.history_matrices.append(self.matrix)
                self.update_grid_cells()
                done = False
                outcome =  l.game_state(self.matrix)
                if outcome == "win":
                    self.grid_cells[1][1].configure(text="You", bg=EMPTY_CELL_COLOR)
                    self.grid_cells[1][2].configure(text="Win!", bg=EMPTY_CELL_COLOR)
                elif outcome == "lose":
                    self.grid_cells[1][1].configure(text="You", bg=EMPTY_CELL_COLOR)
                    self.grid_cells[1][2].configure(text="Lose!", bg=EMPTY_CELL_COLOR)

    def generate_next(self):
        index = (self.gen(), self.gen())
        while self.matrix[index[0], index[1]] != 0:
            index = (self.gen(), self.gen())
        self.matrix[index[0]][index[1]] = 2

game = Window()
