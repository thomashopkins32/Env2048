'''
Contributor(s): Thomas Hopkins

Contains the logic required to create the game 2048.
'''

def new_game():
    '''
    Creates a new game of 2048.
    '''
    matrix = []
    for _ in range(4):
        matrix.append([0]*4)
    return matrix


def add_new(matrix, rand):
    '''
    Adds a new tile in a random free location on game board
    90% chance for 2, 10% chance for 4
    '''
    i = rand.randint(0, 4)
    j = rand.randint(0, 4)
    while matrix[i][j] != 0:
        i = rand.randint(0, 4)
        j = rand.randint(0, 4)
    distribution = [2] * 9 + [4]
    value = rand.choice(distribution)
    matrix[i][j] = value
    return matrix

def game_state(matrix):
    '''
    Determines whether a player has won, lost, or can continue.
    Called after each move made.
    '''
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

def check_col(j, matrix, highest):
    '''
    Checks the column for top 4 numbered tiles and increases fitness
    '''
    add_score = 0
    for k in range(4):
        if matrix[k][j] in highest[:4] and matrix[k][j] != highest[0]:
            add_score += 10
    return add_score

def check_row(i, matrix, highest):
    '''
    Checks the row for top 4 numbered tiles and increases fitness
    '''
    add_score = 0
    for k in range(4):
        if matrix[i][k] in highest[:4] and matrix[i][k] != highest[0]:
            add_score += 25
    return add_score

def calc_score(tile):
    '''
    Calculates score based on the merging of tiles
    '''
    total = 0
    while tile != 2 and tile != 0:
        total += tile
        tile = int(tile/2)
    return total

def score(matrix):
    '''
    Calculates a score representing the "best" game board (fitness function)
    '''
    total_score = 0
    boost = True
    highest = [x for y in matrix for x in y]
    highest = sorted(highest, reverse=True)
    boost = True
    for i in range(4):
        for j in range(4):
            if (i == 0 or i == 3) and matrix[i][j] == highest[0] and boost:
                total_score += 50
                total_score += check_row(i, matrix, highest)
                boost = False
            if (j == 0 or j == 3) and matrix[i][j] == highest[0] and boost:
                total_score += 50
                total_score += check_col(j, matrix, highest)
                boost = False
            total_score += calc_score(matrix[i][j])
    return total_score

def right(board):
    '''
    Moves all tiles to the right and combines same numbered tiles
    '''
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
    '''
    Moves all tiles to the left and combines same numbered tiles
    '''
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
    '''
    Moves all tiles up and combines same numbered tiles
    '''
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
    '''
    Moves all tiles down and combines same numbered tiles
    '''
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
