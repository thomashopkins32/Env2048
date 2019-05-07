from random import randint
import tkinter as tk

class Window(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        self.prompt = tk.Label(self, text="Enter a number:", anchor="w")
        self.entry = tk.Entry(self)
        self.submit = tk.Button(self, text="Submit", command = self.calculate)
        self.output = tk.Label(self, text="")

        self.prompt.pack(side="top", fill="x")
        self.entry.pack(side="top", fill="x", padx=20)
        self.output.pack(side="top", fill="x", expand=True)
        self.submit.pack(side="right")

    def calculate(self):
        try:
            i = int(self.entry.get())
            result = "%s*2=%s" % (i, i*2)
        except ValueError:
            result = "Please enter digits only"
        self.output.configure(text=result)

def right(board):
    for i in range(0, 4, 1):
        for j in range(3, 0, -1):
            for k in range(j-1, -1, -1):
                if board[i][k] != 0:
                    if board[i][j] == board[i][k]:
                        board[i][j] += board[i][k]
                        board[i][k] = 0
                        break
                    elif board[i][j] == 0:
                        board[i][j] = board[i][k]
                        board[i][k] = 0
                    else:
                        break

def left(board):
    for i in range(0, 4, 1):
        for j in range(0, 3, 1):
            for k in range(j+1, 4, 1):
                if board[i][k] != 0:
                    if board[i][j] == board[i][k]:
                        board[i][j] += board[i][k]
                        board[i][k] = 0
                        break
                    elif board[i][j] == 0:
                        board[i][j] = board[i][k]
                        board[i][k] = 0
                    else:
                        break

def up(board):
    for j in range(0, 4, 1):
        for i in range(0, 3, 1):
            for k in range(i+1, 4, 1):
                if board[k][j] != 0:
                    if board[i][j] == board[k][j]:
                        board[i][j] += board[k][j]
                        board[k][j] = 0
                        break
                    elif board[i][j] == 0:
                        board[i][j] = board[k][j]
                        board[k][j] = 0
                    else:
                        break

def down(board):
    for j in range(0, 4, 1):
        for i in range(3, 0, -1):
            for k in range(i-1, -1, -1):
                if board[k][j] != 0:
                    if board[i][j] == board[k][j]:
                        board[i][j] += board[k][j]
                        board[k][j] = 0
                        break
                    elif board[i][j] == 0:
                        board[i][j] = board[k][j]
                        board[k][j] = 0
                    else:
                        break

def printBoard(board):
    for i in board:
        print("\n")
        for j in i:
            print("%5d " % j, end =" ")
    print("\n")


def main():
    root = tk.Tk()
    Window(root).pack(fill="both", expand=True)
    root.mainloop()
    board = [[0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0]]
    for i in range(0,2,1):
        firstI = randint(0,3)
        firstJ = randint(0,3)
        if board[firstI][firstJ] == 0:
            board[firstI][firstJ] = 2
    while True:
        printBoard(board)
        control = input("Pick a direction (type exit to end game): ")
        if control == "r" or control == "right":
            right(board)
        elif control == "l" or control == "left":
            left(board)
        elif control == "u" or control == "up":
            up(board)
        elif control == "d" or control == "down":
            down(board)
        elif control == "exit":
            break
        else:
            print("Try again!")
            continue
        found = False
        while not found:
            i = randint(0,3)
            j = randint(0,3)
            if(board[i][j] == 0):
                board[i][j] = 2
                found = True

if __name__ == '__main__':
    main()
