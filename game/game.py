'''
Contributor(s): Thomas Hopkins

Contains the logic required to create the game 2048.
'''
from numpy import random

class GameState():
    def __init__(self, state=[], lost=False):
        '''
        Create new empty 4x4 board and add two tiles to game
        '''
        if state == []:
            self.matrix = [[0]*4 for _ in range(4)]
            self.add_new()
            self.add_new()
        else:
            self.matrix = state
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

    def perform_multiple_actions(self, actions=[]):
        '''
        Simulates results of multiple actions 
        and returns new GameState
        '''
        game_state = self
        for action in actions:
            game_state = game_state.perform_action(action)
        return game_state

    def perform_action(self, action):
        '''
        Simulates the result of taking a single action 
        and returns a new GameState
        '''
        if self.lost:
            return self
        tmp = self.get_board()
        if action == 'Right':
            self.right()
        elif action == 'Left':
            self.left()
        elif action == 'Down':
            self.down()
        elif action == 'Up':
            self.up()
        else:
            print('action: ' + action + ', not a valid action')
        # check for board change before adding new tile
        if tmp != self.matrix:
            self.add_new()
        if self.game_lost():
            print('You Lost!')
            return GameState(state=self.matrix, lost=True)
        return GameState(state=self.matrix)


    def right(self):
        '''
        Moves all tiles to the right and combines same numbered tiles
        '''
        for i in range(0, 4, 1):
            for j in range(3, 0, -1):
                for k in range(j-1, -1, -1):
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
                for k in range(j+1, 4, 1):
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
                for k in range(i+1, 4, 1):
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
                for k in range(i-1, -1, -1):
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