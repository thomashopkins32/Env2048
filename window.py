import tkinter as tk
import logic

GEOMETRY = '800x1000'

class Window(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.geometry(GEOMETRY)
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
                layout[i][j].grid(row=i, column=j, sticky='news')

    def create_header_widgets(self, header):
        score = tk.Label(header, text='Score: ', justify=tk.CENTER, font=('Helvetica', 18), bg='gray')
        gen = tk.Label(header, text='Generation: ', justify=tk.CENTER, font=('Helvetica', 18), bg='gray')
        score.pack()
        gen.pack()

    def create_content_grid(self, content):
        layout = []
        for i in range(4):
            tmp = []
            for j in range(4):
                tmp.append(tk.Label(content, bg='white', text='0', font=('Helvetica', 18)))
            layout.append(tmp)
        col_weights = [25, 25, 25, 25]
        row_weights = [25, 25, 25 ,25]
        self.create_grid(content, layout=layout, r_weights=row_weights, c_weights=col_weights)


root = tk.Tk()
window = Window(master=root)
window.mainloop()
