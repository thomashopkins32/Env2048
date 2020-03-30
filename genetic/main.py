'''
Contributor(s): Thomas Hopkins

Driver module for 2048AI program
'''
import tkinter as tk
from game.window import Application

def main():
	'''
	Builds application and runs main loop
	'''
	print('Populating...')
	root = tk.Tk()
	app = Application(master=root)
	app.mainloop()

if __name__ == '__main__':
    main()
