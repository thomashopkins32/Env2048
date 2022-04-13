import numpy as np
import gym
from gym import spaces
import pygame

class Env2048(gym.Env):
    # NOTE: PRIVATE methods may change the state of the game, use at your own risk
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 4}

    def __init__(self, size=4, reward_type='survival', seed=None):
        '''
        Initializes the environment.

        Parameters
        ----------
        size : int, optional
            Size of the game board (size x size)
        reward_type : str, optional
            Type of rewards to return on each call to step().
            More information can be found in the step() documentation.
            Supports: {'survival', 'score', 'milestone'}
        seed : int, optional
            Manual random seed
        '''
        super().__init__()

        self.size = size
        self.window_size = 512 # PyGame window size

        # set of possible actions {0: left, 1: right, 2: up, 3: down}
        # highest possible tile is 2 ** 17 according to Wikipedia
        self.observation_space = spaces.Box(low=0, high=float('inf'),
                                            shape=(self.size, self.size),
                                            dtype=np.int32, seed=seed)
        self.action_space = spaces.Discrete(4, seed=seed)
        self.window = None
        self.clock = None
        self.score = 0
        self.done = False
        self.reward_type = reward_type

        self._color_dict = {0: (255, 255, 255),
                            2: (238, 228, 218),
                            4: (237, 224, 200),
                            8: (242, 177, 121),
                            16: (245, 149, 99),
                            32: (246, 124, 95),
                            64: (246, 94, 59),
                            128: (237, 207, 114),
                            256: (237, 204, 97),
                            512: (237, 200, 80),
                            1024: (237, 197, 63),
                            2048: (237, 194, 46)}

    def _get_obs(self):
        ''' Returns the current state of the game '''
        return self._state

    def _get_info(self):
        ''' Returns information about the state of the current game '''
        return {'score': self.score,
                'max': np.max(self._state),
                'min': np.min(self._state),
                'avg': np.mean(self._state)}

    def _is_lost(self):
        '''
        PRIVATE METHOD

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

    def _add_tile(self):
        '''
        PRIVATE METHOD

        Adds either a 2 or 4 to the board
        with probability 0.9 of a 2

        Modifies
        --------
        self._state : np.array
            adds a new tile to the current state
        '''
        if self.done:
            return
        possible_tiles = np.argwhere(self._state == 0)
        random_idx = np.random.randint(0, possible_tiles.shape[0])
        tile = possible_tiles[random_idx]
        if np.random.rand() < 0.9:
            self._state[tile[0], tile[1]] = 2
        else:
            self._state[tile[0], tile[1]] = 4

    def _rotate(self, action, reverse=False):
        '''
        PRIVATE METHOD

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
        PRIVATE METHOD

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
        PRIVATE METHOD

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

    def reset(self, seed=None, return_info=False, options=None):
        '''
        Resets the environment to create a new game

        Parameters
        ----------
        seed : int, optional
            control for randomness in tile placement
        return_info : bool, optional
            if True, return information about the start of the game
        options : Dict, optional
            Miscellaneuous options, currently does nothing

        Returns
        -------
        np.array
            new game board
        dict, optional
            if return_info = True, information about the new board
        '''
        super().reset(seed=seed)

        self._state = np.zeros((self.size, self.size), dtype=np.int32)
        self._add_tile()
        self._add_tile()
        self.score = 0
        self.done = False

        observation = self._get_obs()
        info = self._get_info()

        return (observation, info) if return_info else observation

    def step(self, action):
        '''
        Makes a move in a given direction and adds to
        the score of the current game.

        Here are the different reward options (set in __init__):
        'survival':
            Any valid move that changes state get +1 reward.
            Game over results in 0 reward.
            Moves that don't change state get -0.1 reward.
        'score':
            Reward is simply the amount added to the traditional
            game score. This is calculated as the sum of all
            tiles merged during this action.
        'milestone':
            A reward of +10 is given every time a new maximum tile
            has been reached. All other moves give 0 reward.

        Parameters
        ----------
        action : int
            0 : left, 1 : up, 2: right, 3 : down

        Returns
        -------
        observation : np.array
            state of the board after the action
        reward : float
            signal for reinforcement
        done : bool
            True if game is over, False otherwise
        info : dict
            Additional info about state of the board
        '''
        if self.done:
            return self._get_obs(), 0.0, True, self._get_info()

        # copy state to check when action does nothing
        prev_state = np.copy(self._state)

        # a single move is a rotate, flush, merge, flush, rotate back
        self._rotate(action)
        self._flush()
        score_change = self._merge()
        self._flush()
        self._rotate(action, reverse=True)

        # check for change in state
        changed = not np.array_equal(prev_state, self._state)

        # no need to check if no change in state
        if changed:
            self.done = self._is_lost()

        # update score
        self.score += score_change

        # calculate reward
        if self.reward_type == 'survival':
            if not changed:
                reward = -0.1
            else:
                reward = 1.0
        elif self.reward_type == 'score':
            reward = score_change
        elif self.reward_type == 'milestone':
            if np.max(self._state) > self._curr_max:
                reward = 10.0
            else:
                reward = 0.0
        if self.done:
            reward = 0.0

        # only add a new tile if the game state changed
        if changed:
            self._add_tile()

        # add info about change in state
        info = self._get_info()
        info['changed'] = changed

        return self._get_obs(), reward, self.done, info

    def render(self, mode="human"):
        '''
        Displays the state of the board in a PyGame window

        Parameters
        ----------
        mode : str
            Display mode for rendering.
            "human": display PyGame window with game board
            "rgb_array': return 3D pixel array
            Supports: {'human', 'rgb_array'}

        Returns
        -------
        pixel_array : np.array
            If mode = 'rgb_array' then this is returned.
        '''
        if self.window is None and mode == 'human':
            pygame.init()
            pygame.display.init()
            self.window = pygame.display.set_mode((self.window_size, self.window_size))
        if self.clock is None and mode == 'human':
            self.clock = pygame.time.Clock()

        canvas = pygame.Surface((self.window_size, self.window_size))
        canvas.fill((255, 255, 255))
        pix_square_size = self.window_size / self.size

        # draw the squares and values
        for i in range(self.size):
            for j in range(self.size):
                num = self._state[i, j]
                if num not in self._color_dict:
                    color = (50, 50, 50)
                else:
                    color = self._color_dict[num]
                if num == 0:
                    s = ''
                else:
                    s = str(num)
                rect = pygame.draw.rect(
                    canvas,
                    color,
                    pygame.Rect(
                        pix_square_size * np.array([i, j]),
                        (pix_square_size, pix_square_size),
                    ),
                )
                text = pygame.font.SysFont('Arial', 20).render(
                    s,
                    True,
                    (0, 0, 0),
                )
                text_rect = text.get_rect(center=rect.center)
                canvas.blit(text, text_rect)

        for i in range(self.size + 1):
            pygame.draw.line(
                canvas,
                0,
                (0, pix_square_size * i),
                (self.window_size, pix_square_size * i),
                width=3,
            )
            pygame.draw.line(
                canvas,
                0,
                (pix_square_size * i, 0),
                (pix_square_size * i, self.window_size),
                width=3
            )

        if mode == 'human':
            self.window.blit(canvas, canvas.get_rect())
            pygame.event.pump()
            pygame.display.update()

            self.clock.tick(self.metadata['render_fps'])
        else:
            return np.transpose(
                np.array(pygame.surfarray.pixels3d(canvas)), axes=(1, 0, 2)
            )

    def close(self):
        if self.window is not None:
            pygame.display.quit()
            pygame.quit()
