from constants import *

# creates a new game of 2048
def new_game():
    matrix = []
    for i in range(4):
        matrix.append([0]*4)
    return matrix

# adds a new tile in a random free location on game board
# 90% chance for 2, 10% chance for 4
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

# determines whether a player has won, lost, or can continue
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

# checks the column for top 4 numbered tiles and increases fitness
def check_col(j, matrix, highest):
    score = 0
    for k in range(4):
        if matrix[k][j] in highest[:4] and matrix[k][j] != highest[0]:
            score += 10
    return score

# checks the row for top 4 numbered tiles and increases fitness
def check_row(i, matrix, highest):
    score = 0
    for k in range(4):
        if matrix[i][k] in highest[:4] and matrix[i][k] != highest[0]:
            score += 25
    return score

# calculates score based on the merging of tiles
def calc_score(score):
    sum = 0
    while score != 2 and score != 0:
        sum += score
        score = int(score/2)
    return sum

# calculates a score representing the "best" game board (fitness function)
def score(matrix):
    score = 0
    boost = True
    highest = [x for y in matrix for x in y]
    highest = sorted(highest, reverse=True)
    boost = True
    for i in range(4):
        for j in range(4):
            if (i == 0 or i == 3) and matrix[i][j] == highest[0] and boost:
                score += 50
                score += check_row(i, matrix, highest)
                boost = False
            if (j == 0 or j == 3) and matrix[i][j] == highest[0] and boost:
                score += 50
                score += check_col(j, matrix, highest)
                boost = False
            score += calc_score(matrix[i][j])
    return score

# moves all tiles to the right and combines same numbered tiles
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

# moves all tiles to the left and combines same numbered tiles
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

# moves all tiles up and combines same numbered tiles
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

# moves all tiles down and combines same numbered tiles
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
