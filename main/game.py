import numpy as np
import copy

class GameState:
    def __init__(self, state=None, score=0):
        if state is None:
            self.state = np.zeros((4,4), dtype=int)
        else:
            self.state = copy.deepcopy(state)
        self.score = score
        

    def _add_tile(self, state):
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
        Makes a move in a given direction and adds to
        the score of the current game
        
        Parameters
        ----------
        direction : str
            left, right, up, or down

        Returns
        -------
        GameState
            merges tiles in specified direction,
            adds one new tile, and adds to the score
        '''
        pass


    def _merge(self, state, direction):
        '''
        PRIVATE FUNCTION

        Merges same tiles in given direction and
        calculates score of merge. Score is determined
        by the value of the tile after merging.
        So, 8 merged with 8 gives a score of 16.

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
        int
            total score accrued during merge
        '''
        pass

