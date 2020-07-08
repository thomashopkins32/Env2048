'''
Contributor(s): Thomas Hopkins

Contains the logic required to create the game 2048.
'''
from numpy import random

from game.constants import POSITION_TABLE


class GameState():
    def __init__(self, state=[], lost=False):
        '''
        Create new empty 4x4 board and add two tiles to game
        '''
        if state == []:
            self.matrix = [[0] * 4 for _ in range(4)]
            self.add_new()
            self.add_new()
        else:
            self.matrix = [x[:] for x in state]
        self.lost = lost

    def __iter__(self):
        return iter(self.matrix)

    def get_board(self):
        '''
        Returns the current state of the board (unmutable)
        '''
        return [x[:] for x in self.matrix]

    def game_lost(self):
        '''
        Determines whether a player has lost the game.
        Called after each move made.
        Returns True if game has been lost and False otherwise
        '''
        if self.lost:
            return True
        fill_count = 0
        check_failure = False
        for i in range(4):
            if 0 not in self.matrix[i]:
                fill_count += 1
        if fill_count == 4:
            check_failure = True
        else:
            return False
        if check_failure:
            tmp = GameState(state=self.get_board())
            tmp.right()
            tmp.left()
            tmp.up()
            tmp.down()
            if tmp.matrix == self.matrix:
                return True
        return False

    def add_new(self):
        '''
        Adds a new tile in a random free location on game board
        90% chance for 2, 10% chance for 4
        '''
        # check if adding a new is possible (useful for moves that dont shift anything)
        i = random.randint(0, 4)
        j = random.randint(0, 4)
        while self.matrix[i][j] != 0:
            i = random.randint(0, 4)
            j = random.randint(0, 4)
        distribution = [2] * 9 + [4]
        value = random.choice(distribution)
        self.matrix[i][j] = value

    def perform_multiple_actions(self, actions=''):
        '''
        Simulates results of multiple actions 
        and returns new GameState
        '''
        for action in actions:
            self.perform_action(action)
        return self.get_board()

    def perform_action(self, action):
        '''
        Simulates the result of taking a single action 
        and modifies state in place
        '''
        if self.lost:
            return
        tmp = self.get_board()
        if action == 'Right' or action == 'R':
            self.right()
        elif action == 'Left' or action == 'L':
            self.left()
        elif action == 'Down' or action == 'D':
            self.down()
        elif action == 'Up' or action == 'U':
            self.up()
        else:
            print('action: ' + action + ', not a valid action')
        # check for board change before adding new tile
        if tmp != self.matrix:
            self.add_new()
        if self.game_lost():
            self.lost = True

    def generate_successor(self, action):
        '''
        Simulates the result of taking a single action
        and returns a new GameState
        '''
        if self.lost:
            return self
        tmp = self.get_board()
        self.perform_action(action)
        # reset lost
        if self.lost:
            self.lost = False
        successor = self.get_board()
        self.matrix = tmp
        return GameState(state=successor)

    def possible_random_states(self):
        states = []
        zero_count = 0
        for i in range(4):
            for j in range(4):
                if self.matrix[i][j] == 0:
                    zero_count += 1
                    board2 = self.get_board()
                    board4 = self.get_board()
                    board2[i][j] = 2
                    board4[i][j] = 4
                    board2 = GameState(state=board2)
                    board4 = GameState(state=board4)
                    states.append([board2, .9])
                    states.append([board4, .1])
        # adjust probabilities of all states
        if zero_count != 0:
            adjust = 1 / zero_count
        else:
            adjust = 0
        for state in states:
            state[1] = state[1] * adjust
        return states

    def get_score(self):
        if self.game_lost():
            return 0
        board = self.matrix
        position_heuristic = 0
        for i in range(4):
            for j in range(4):
                position_heuristic += board[i][j] * POSITION_TABLE[i][j]
        difference_penalty = 0
        for i in range(4):
            for j in range(4):
                neighbors = [(i+1, j), (i-1, j), (i, j+1), (i, j-1)]
                for (ni, nj) in neighbors:
                    if ni < 0 or ni >= 4 or nj < 0 or nj >= 4:
                        continue
                    difference_penalty += abs(board[i][j] - board[ni][nj])
        difference_penalty = -difference_penalty
        increasing_along_edge = 0
        bottom_edge = sorted(board[3])
        if bottom_edge == board[3]:
            increasing_along_edge += 100
        right_edge = sorted(board[:][3])
        if right_edge == board[:][3]:
            increasing_along_edge += 100
        return 5*position_heuristic + 1*difference_penalty + 5*increasing_along_edge

    def right(self):
        '''
        Moves all tiles to the right and combines same numbered tiles
        '''
        for i in range(0, 4, 1):
            for j in range(3, 0, -1):
                for k in range(j - 1, -1, -1):
                    if self.matrix[i][k] != 0:
                        if self.matrix[i][j] == self.matrix[i][k]:
                            self.matrix[i][j] += self.matrix[i][k]
                            self.matrix[i][k] = 0
                            break
                        elif self.matrix[i][j] == 0:
                            self.matrix[i][j] = self.matrix[i][k]
                            self.matrix[i][k] = 0
                        else:
                            break

    def left(self):
        '''
        Moves all tiles to the left and combines same numbered tiles
        '''
        for i in range(0, 4, 1):
            for j in range(0, 3, 1):
                for k in range(j + 1, 4, 1):
                    if self.matrix[i][k] != 0:
                        if self.matrix[i][j] == self.matrix[i][k]:
                            self.matrix[i][j] += self.matrix[i][k]
                            self.matrix[i][k] = 0
                            break
                        elif self.matrix[i][j] == 0:
                            self.matrix[i][j] = self.matrix[i][k]
                            self.matrix[i][k] = 0
                        else:
                            break

    def up(self):
        '''
        Moves all tiles up and combines same numbered tiles
        '''
        for j in range(0, 4, 1):
            for i in range(0, 3, 1):
                for k in range(i + 1, 4, 1):
                    if self.matrix[k][j] != 0:
                        if self.matrix[i][j] == self.matrix[k][j]:
                            self.matrix[i][j] += self.matrix[k][j]
                            self.matrix[k][j] = 0
                            break
                        elif self.matrix[i][j] == 0:
                            self.matrix[i][j] = self.matrix[k][j]
                            self.matrix[k][j] = 0
                        else:
                            break

    def down(self):
        '''
        Moves all tiles down and combines same numbered tiles
        '''
        for j in range(0, 4, 1):
            for i in range(3, 0, -1):
                for k in range(i - 1, -1, -1):
                    if self.matrix[k][j] != 0:
                        if self.matrix[i][j] == self.matrix[k][j]:
                            self.matrix[i][j] += self.matrix[k][j]
                            self.matrix[k][j] = 0
                            break
                        elif self.matrix[i][j] == 0:
                            self.matrix[i][j] = self.matrix[k][j]
                            self.matrix[k][j] = 0
                        else:
                            break
