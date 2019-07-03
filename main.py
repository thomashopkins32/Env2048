import tkinter as tk
from window import *

def main():
    root = tk.Tk()
    window = Window(master=root)
    window.mainloop()

if __name__ == '__main__':
    main()
