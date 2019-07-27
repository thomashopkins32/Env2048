import tkinter as tk
from window import *

# driver function
def main():
    print('Populating...')
    root = tk.Tk()
    window = Window(master=root)
    window.mainloop()

if __name__ == '__main__':
    main()
