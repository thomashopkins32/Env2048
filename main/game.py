import numpy as np


class GameState:
    def __init__(self, state=None):
        self.state = np.zeros((4,4), dtype=int) 
        

    def add_tile(self, state):
        '''
        PRIVATE FUNCTION

        Adds either a 2 or 4 to the board
        with probability 0.9 of a 2

        Parameters
        ----------
        state : np.array
            board to modify

        Returns
        -------
        np.array
            the state of the array after adding
            a new tile
        '''
#        possible_tiles = np.argwhere(self.state == 0)
 #       to_add = min(n, possible_tiles.shape[0])
        pass


    def move(self, direction):
        '''
        Makes a move in a given direction
        
        Parameters
        ----------
        direction : str
            left, right, up, or down

        Returns
        -------
        GameState
            merges tiles in specified direction
            and adds one new tile
        '''
        pass


    def merge(self, state, direction):
        '''
        PRIVATE FUNCTION

        Merges same tiles in given direction

        Parameters
        ----------
        state : np.array
            array to merge tiles
        direction : str
            left, right, up, down

        Returns
        -------
        np.array
            the state of the array after merging
        '''
        pass


    def score(self):
        '''
        Calculates the score of the current
        '''
        pass

