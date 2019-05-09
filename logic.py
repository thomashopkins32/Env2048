from random import randint

def new_game():
    matrix = []
    for i in range(4):
        matrix.append([0]*4)
    return matrix

def add_two(matrix):
    x = randint(0, len(matrix)-1)
    y = randint(0, len(matrix)-1)
    while(matrix[x][y] != 0):
        x = randint(0, len(matrix)-1)
        y = randint(0, len(matrix)-1)
    matrix[x][y] = 2
    return matrix

def game_state(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if matrix[i][j] == 2048:
                return "win"
    for i in range(len(matrix)-1):
        for j in range(len(matrix[0])-1):
            if matrix[i][j] == matrix[i+1][j] or matrix[i][j] == matrix[i][j+1]:
                return ""
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == 0:
                return ""
    for i in range(len(matrix)-1):
        if matrix[len(matrix)-1][k] == matrix[len(matrix)-1][k+1]:
            return ""
        if matrix[k][len(matrix)-1] == matrix[k+1][len(matrix)-1]:
            return ""
    return "lose"


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
