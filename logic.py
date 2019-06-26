from numpy import random

def new_game():
    matrix = []
    for i in range(4):
        matrix.append([0]*4)
    return matrix

def add_new(matrix):
    i = random.randint(0, 4)
    j = random.randint(0, 4)
    while matrix[i][j] != 0:
        i = random.randint(0, 4)
        j = random.randint(0, 4)
    distribution = [2] * 9 + [4]
    value = random.choice(distribution)
    matrix[i][j] = value
    return matrix

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
    return board

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
    return board

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
    return board

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
    return board
