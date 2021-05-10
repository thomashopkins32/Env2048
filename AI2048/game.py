import numpy as np


class GameState:
    def __init__(self, size=4):
        self.state = np.zeros((size, size), dtype=int)
        self._add_tile()
        self._add_tile()
        self.score = 0
        self.size = size
        self.lost = self.is_lost()

    def _add_tile(self):
        '''
        PRIVATE FUNCTION

        Adds either a 2 or 4 to the board
        with probability 0.9 of a 2

        Modifies
        --------
        self.state : np.array
            adds a new tile to the current state
        '''
        possible_tiles = np.argwhere(self.state == 0)
        random_idx = np.random.randint(0, possible_tiles.shape[0])
        tile = possible_tiles[random_idx]
        if np.random.rand() < 0.9:
            self.state[tile[0], tile[1]] = 2
        else:
            self.state[tile[0], tile[1]] = 4

    def is_lost(self):
        '''
        Determines if the current state of the
        board is in a lost position

        Returns
        -------
        bool
            True if a merge or flush is possible
            False otherwise
        '''
        if np.count_nonzero(self.state == 0) > 0:
            return False
        # check for adjacent matching
        # tiles in 4 directions at each tile
        for i in range(self.size):
            for j in range(self.size):
                # left
                if j-1 >= 0:
                    if self.state[i][j] == self.state[i][j-1]:
                        return False
                # right
                if j+1 < self.size:
                    if self.state[i][j] == self.state[i][j+1]:
                        return False
                # up
                if i-1 >= 0:
                    if self.state[i][j] == self.state[i-1][j]:
                        return False
                # down
                if i+1 < self.size:
                    if self.state[i][j] == self.state[i+1][j]:
                        return False
        return True

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
        int
            score from this move
        '''
        if self.lost:
            return 0
        prev_state = np.copy(self.state)
        # move is a rotate, flush, merge, flush, rotate back
        self._rotate(direction)
        self._flush()
        score = self._merge()
        self._flush()
        self._rotate(direction, reverse=True)
        self.lost = self.is_lost()
        self.score += score
        if np.array_equal(prev_state, self.state) or self.lost:
            return score
        # add tile
        self._add_tile()
        return score

    def _rotate(self, direction, reverse=False):
        '''
        PRIVATE FUNCTION

        Rotates the tiles so the direction
        of interest is "left". Useful for merging and flushing

        Parameters
        ----------
        direction : str
            direction to determine rotation angle
        reverse : bool, optional
            flag to rotate back to original direction
        '''
        rotation_dict = {'right': 2,
                         'left': 0,
                         'up': 1,
                         'down': 3}
        num_rotations = rotation_dict[direction]
        if reverse:
            num_rotations = 4 - num_rotations
        self.state = np.rot90(self.state, k=num_rotations)

    def _merge(self):
        '''
        PRIVATE FUNCTION

        Merges same tiles in the left direction and
        calculates score of merge. Score is determined
        by the value of the tile after merging.
        So, 8 merged with 8 gives a score of 16.

        Modifies
        --------
        self.state : np.array
            merges the tiles in the current state

        Returns
        -------
        int
            total score accrued during merge
        '''
        score = 0
        # perform left merge
        for i in range(self.size):
            for j in range(self.size):
                if self.state[i][j] != 0:
                    for k in range(j+1, self.size):
                        if self.state[i][j] == self.state[i][k]:
                            value = 2*self.state[i][j]
                            self.state[i][j] = value
                            self.state[i][k] = 0
                            score += value
                            break
                        if self.state[i][k] != 0:
                            break
        return score

    def _flush(self):
        '''
        PRIVATE FUNCTION

        Moves the tiles along empty space, 0s, in
        the left direction

        Modifies
        --------
        self.state : np.array
            moves tiles in current state
        '''
        # peform left flush
        for i in range(self.size):
            for j in range(self.size):
                if self.state[i][j] == 0:
                    for k in range(j+1, self.size):
                        if self.state[i][k] != 0:
                            self.state[i][j] = self.state[i][k]
                            self.state[i][k] = 0
                            break
        return self.state
