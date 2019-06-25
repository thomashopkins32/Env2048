import tkinter as tk
import logic

GEOMETRY = '800x1000'

class Window(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.init_window()

        self.matrix = logic.new_game()
        self.matrix = logic.add_new(self.matrix)
        self.matrix = logic.add_new(self.matrix)

    def init_window(self):
        self.master.geometry(GEOMETRY)
        self.master.title('2048')
        self.master.bind('<Key>', self.key_pressed)
        self.header = tk.Frame(self.master, bg='gray')
        self.create_header_widgets(self.header)

        self.content = tk.Frame(self.master, bg='gray')
        self.create_content_grid(self.content)

        layout = [[self.header], [self.content]]
        col_weights = [1]
        row_weights = [1, 99]
        self.create_grid(self.master, layout=layout, r_weights=row_weights, c_weights=col_weights)

    def create_grid(self, container, layout=[], r_weights=[], c_weights=[]):
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

    def create_header_widgets(self, header):
        self.score = tk.Label(header, text='Score: ', justify=tk.CENTER, font=('Helvetica', 18), bg='gray')
        self.gen = tk.Label(header, text='Generation: ', justify=tk.CENTER, font=('Helvetica', 18), bg='gray')
        self.score.pack()
        self.gen.pack()

    def create_content_grid(self, content):
        self.labels = []
        for i in range(4):
            tmp = []
            for j in range(4):
                tmp.append(tk.Label(content, bg='white', text='0', font=('Helvetica', 24), borderwidth=2, relief='raised' ))
            self.labels.append(tmp)
        col_weights = [25, 25, 25, 25]
        row_weights = [25, 25, 25 ,25]
        self.create_grid(content, layout=self.labels, r_weights=row_weights, c_weights=col_weights)

    def update_labels(self):
        for i in range(4):
            for j in range(4):
                new_value = self.matrix[i][j]
                if new_value == 0:
                    self.labels[i][j].configure(text='0', bg='white')
                else:
                    self.labels[i][j].configure(text=str(new_value))
        self.update_idletasks()

    def key_pressed(self, event):
        if event.keysym == 'Right':
            self.matrix = logic.right(self.matrix)
        elif event.keysym == 'Left':
            self.matrix = logic.left(self.matrix)
        elif event.keysym == 'Down':
            self.matrix = logic.down(self.matrix)
        elif event.keysym == 'Up':
            self.matrix = logic.up(self.matrix)
        self.update_labels()
        self.matrix = logic.add_new(self.matrix)

root = tk.Tk()
window = Window(master=root)
window.mainloop()
