
import tkinter as tk
from game.window import Application

if __name__ == '__main__':
	root = tk.Tk()
	app = Application(master=root, option='manual')
	app.mainloop()