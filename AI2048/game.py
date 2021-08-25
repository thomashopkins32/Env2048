import numpy as np
from tf_agents.environments import py_environment
from tf_agents.specs import array_spec
from tf_agents.trajectories import time_step as ts


class Env2048(py_environment.PyEnvironment):
    def __init__(self, size=4):
        super(Env2048, self).__init__()
        # set of possible actions {0: left, 1: right, 2: up, 3: down}
        self._action_spec = array_spec.BoundedArraySpec(shape=(), dtype=np.int32,
                                                        minimum=0, maximum=3,
                                                        name='action')
        self._observation_spec = array_spec.BoundedArraySpec(shape=(size, size),
                                                             dtype=np.int32,
                                                             name='observation')
        self._state = np.zeros((size, size), dtype=np.int32)
        self._episode_ended = self.is_lost()
        self._add_tile()
        self._add_tile()
        self.score = 0
        self.size = size

    def action_spec(self):
        return self._action_spec

    def observation_spec(self):
        return self._observation_spec

    def _reset(self):
        self._state = np.zeros((self.size, self.size), dtype=np.int32)
        self._add_tile()
        self._add_tile()
        self.score = 0
        return ts.restart(np.array(self._state, dtype=np.int32))

    def _add_tile(self):
        '''
        PRIVATE FUNCTION

        Adds either a 2 or 4 to the board
        with probability 0.9 of a 2

        Modifies
        --------
        self._state : np.array
            adds a new tile to the current state
        '''
        possible_tiles = np.argwhere(self._state == 0)
        random_idx = np.random.randint(0, possible_tiles.shape[0])
        tile = possible_tiles[random_idx]
        if np.random.rand() < 0.9:
            self._state[tile[0], tile[1]] = 2
        else:
            self._state[tile[0], tile[1]] = 4

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
        if np.count_nonzero(self._state == 0) > 0:
            return False
        # check for adjacent matching
        # tiles in 4 directions at each tile
        for i in range(self.size):
            for j in range(self.size):
                # left
                if j-1 >= 0:
                    if self._state[i][j] == self._state[i][j-1]:
                        return False
                # right
                if j+1 < self.size:
                    if self._state[i][j] == self._state[i][j+1]:
                        return False
                # up
                if i-1 >= 0:
                    if self._state[i][j] == self._state[i-1][j]:
                        return False
                # down
                if i+1 < self.size:
                    if self._state[i][j] == self._state[i+1][j]:
                        return False
        return True

    def _step(self, action):
        '''
        Makes a move in a given direction and adds to
        the score of the current game

        Parameters
        ----------
        action : int
            0 : left, 1 : up, 2: right, 3 : down

        Returns
        -------
        int
            score from this move
        '''
        if self._episode_ended:
            return self.reset()
        prev_state = np.copy(self._state)
        # move is a rotate, flush, merge, flush, rotate back
        self._rotate(action)
        self._flush()
        reward = self._merge()
        self._flush()
        self._rotate(action, reverse=True)
        self._episode_ended = self.is_lost()
        self.score += reward
        if np.array_equal(prev_state, self._state):
            return ts.transition(np.array(self._state, dtype=np.int32),
                                 reward=-1.0, discount=1.0)
        if self._episode_ended:
            return ts.termination(np.array(self._state, dtype=np.int32), -100.0)
        # add tile
        self._add_tile()
        return ts.transition(np.array(self._state, dtype=np.int32), reward=reward, discount=1.0)

    def _rotate(self, action, reverse=False):
        '''
        PRIVATE FUNCTION

        Rotates the tiles so the direction
        of interest is "left". Useful for merging and flushing

        Parameters
        ----------
        action : int
            direction to determine rotation angle
            0 : left, 1 : up, 2 : right, 3 : down
        reverse : bool, optional
            flag to rotate back to original direction
        '''
        num_rotations = action
        if reverse:
            num_rotations = 4 - num_rotations
        self._state = np.rot90(self._state, k=num_rotations)

    def _merge(self):
        '''
        PRIVATE FUNCTION

        Merges same tiles in the left direction and
        calculates score of merge. Score is determined
        by the value of the tile after merging.
        So, 8 merged with 8 gives a score of 16.

        Modifies
        --------
        self._state : np.array
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
                if self._state[i][j] != 0:
                    for k in range(j+1, self.size):
                        if self._state[i][j] == self._state[i][k]:
                            value = 2*self._state[i][j]
                            self._state[i][j] = value
                            self._state[i][k] = 0
                            score += value
                            break
                        if self._state[i][k] != 0:
                            break
        return score

    def _flush(self):
        '''
        PRIVATE FUNCTION

        Moves the tiles along empty space, 0s, in
        the left direction

        Modifies
        --------
        self._state : np.array
            moves tiles in current state
        '''
        # peform left flush
        for i in range(self.size):
            for j in range(self.size):
                if self._state[i][j] == 0:
                    for k in range(j+1, self.size):
                        if self._state[i][k] != 0:
                            self._state[i][j] = self._state[i][k]
                            self._state[i][k] = 0
                            break
