import numpy as np
import copy


class GameState:
    def __init__(self, state=None, score=0):
        if state is None:
            state = np.zeros((4, 4), dtype=int)
            state = self._add_tile(state)
            self.state = self._add_tile(state)
        else:
            self.state = copy.deepcopy(state)
        self.score = score
        self.lost = self.is_lost()

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
        new_state = copy.deepcopy(state)
        possible_tiles = np.argwhere(new_state == 0)
        random_idx = np.random.randint(0, possible_tiles.shape[0])
        tile = possible_tiles[random_idx]
        if np.random.rand() < 0.9:
            new_state[tile[0], tile[1]] = 2
        else:
            new_state[tile[0], tile[1]] = 4
        return new_state

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
        for i in range(4):
            for j in range(4):
                # left
                if j-1 >= 0:
                    if self.state[i][j] == self.state[i][j-1]:
                        return False
                # right
                if j+1 < 4:
                    if self.state[i][j] == self.state[i][j+1]:
                        return False
                # up
                if i-1 >= 0:
                    if self.state[i][j] == self.state[i-1][j]:
                        return False
                # down
                if i+1 < 4:
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
        GameState
            merges tiles in specified direction,
            adds one new tile, and adds to the score
        '''
        if self.lost:
            return self
        # move is a rotate, flush, merge, flush, rotate back
        rotated_state = self._rotate(self.state, direction)
        flushed_state = self._flush(rotated_state)
        merged_state, score = self._merge(flushed_state)
        flushed_state = self._flush(merged_state)
        semi_state = self._rotate(flushed_state, direction, reverse=True)
        # no change
        if np.array_equal(semi_state, self.state):
            return self
        # add tile and score
        full_state = self._add_tile(semi_state)
        full_score = self.score + score
        return GameState(state=full_state, score=full_score)

    def _rotate(self, state, direction, reverse=False):
        '''
        PRIVATE FUNCTION

        Rotates the tiles so the direction
        of interest is "left". Useful for merging and flushing

        Parameters
        ----------
        state : np.array
            current state of the board to rotate
        direction : str
            direction to determine rotation angle
        reverse : bool, optional
            flag to rotate back to original direction

        Returns
        -------
        np.array
            COPY of original state after rotation
        '''
        c_state = copy.deepcopy(state)
        rotation_dict = {'right': 2,
                         'left': 0,
                         'up': 1,
                         'down': 3}
        num_rotations = rotation_dict[direction]
        if reverse:
            num_rotations = 4 - num_rotations
        return np.rot90(c_state, k=num_rotations)

    def _merge(self, state):
        '''
        PRIVATE FUNCTION

        Merges same tiles in the left direction and
        calculates score of merge. Score is determined
        by the value of the tile after merging.
        So, 8 merged with 8 gives a score of 16.

        Parameters
        ----------
        state : np.array
            array to merge tiles

        Returns
        -------
        np.array
            COPY of the state of the array after merging
        int
            total score accrued during merge
        '''
        c_state = copy.deepcopy(state)
        score = 0
        # perform left merge
        for i in range(4):
            for j in range(4):
                if c_state[i][j] != 0:
                    for k in range(j+1, 4):
                        if c_state[i][j] == c_state[i][k]:
                            value = 2*c_state[i][j]
                            c_state[i][j] = value
                            c_state[i][k] = 0
                            score += value
                            break
        return c_state, score

    def _flush(self, state):
        '''
        PRIVATE FUNCTION

        Moves the tiles along empty space, 0s, in
        the left direction

        Parameters
        ----------
        state : np.array
            current state of the board

        Returns
        -------
        np.array
            COPY of the state of the array after
            moving values along empty locations in
            the given direction
        '''
        c_state = copy.deepcopy(state)
        # peform left flush
        for i in range(4):
            for j in range(4):
                if c_state[i][j] == 0:
                    for k in range(j+1, 4):
                        if c_state[i][k] != 0:
                            c_state[i][j] = c_state[i][k]
                            c_state[i][k] = 0
                            break
        return c_state
