from constants import *

def new_game():
    matrix = []
    for i in range(4):
        matrix.append([0]*4)
    return matrix

def add_new(matrix, r):
    i = r.randint(0, 4)
    j = r.randint(0, 4)
    while matrix[i][j] != 0:
        i = r.randint(0, 4)
        j = r.randint(0, 4)
    distribution = [2] * 9 + [4]
    value = r.choice(distribution)
    matrix[i][j] = value
    return matrix

def game_state(matrix):
    fill_count = 0
    check_failure = False
    for i in range(4):
        if 2048 in matrix[i]:
            return 'win'
        if 0 not in matrix[i]:
            fill_count += 1
    if fill_count == 4:
        check_failure = True
    else:
        return 'continue'
    if check_failure:
        tmp = [x[:] for x in matrix]
        matrix = right(matrix)
        matrix = left(matrix)
        matrix = up(matrix)
        matrix = down(matrix)
        if tmp == matrix:
            return 'lose'
    return 'continue'

def is_edge(i, j):
    if i == 0 or j == 0 or i == 3 or j == 3:
        return True
    return False

def calc_score(score):
    sum = 0
    while score != 2 and score != 0:
        sum += score
        score = score/2
    return sum

def score(matrix):
    score = 0
    boost = True
    flat = [x for y in matrix for x in y]
    flat = sorted(flat, reverse=True)
    for i in range(4):
        for j in range(4):
            if matrix[i][j] == flat[0] and is_edge(i, j) and boost:
                score += 30
                # increase fitness for consecutive highest values
                boost = False
            score += calc_score(matrix[i][j])
    score += 2*flat[0] + flat[1]
    return score


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
