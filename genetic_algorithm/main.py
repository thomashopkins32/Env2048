import tkinter as tk
from window import *

def main():
    print('Populating...')
    root = tk.Tk()
    random.seed(22)
    window = Window(master=root)
    window.mainloop()

if __name__ == '__main__':
    main()
