'''
Unit testing for GameState module
'''
import numpy as np
from bitarray import bitarray

from AI2048.game import GameState


def test_new_game():
    game = GameState()
    assert(game.state.shape == (4, 4))
    assert(np.count_nonzero(game.state == 0) == 14)
    assert(np.count_nonzero(game.state < 0) == 0)
    assert(np.count_nonzero(game.state > 0) == 2)
    assert(np.count_nonzero(game.state > 4) == 0)


def test_old_game():
    game = GameState()
    state = np.array([[2, 2, 2, 2],
                      [2, 2, 2, 2],
                      [2, 2, 2, 2],
                      [2, 2, 2, 2]])
    game.state = state
    assert(game.state.shape == (4, 4))
    assert(np.count_nonzero(game.state == 2) == 16)


def test_add_tile():
    game = GameState()
    state = np.array([[0, 0, 0, 0],
                      [0, 0, 0, 0],
                      [0, 0, 0, 0],
                      [0, 0, 0, 0]])
    game.state = state
    game._add_tile()
    assert(np.count_nonzero(game.state == 0) == 15)
    assert(np.count_nonzero(game.state > 4) == 0)
    assert(np.count_nonzero(game.state < 0) == 0)
    two_count = np.count_nonzero(game.state == 2)
    four_count = np.count_nonzero(game.state == 4)
    assert((two_count == 0 and four_count == 1) or
           (two_count == 1 and four_count == 0))


def test_rotate():
    # no rotation (left)
    game = GameState()
    state = np.array([[2, 4, 8, 16],
                      [32, 64, 128, 256],
                      [16, 4, 8, 2],
                      [256, 128, 64, 2]])
    expected = np.array([[2, 4, 8, 16],
                         [32, 64, 128, 256],
                         [16, 4, 8, 2],
                         [256, 128, 64, 2]])
    game.state = state
    game._rotate('left')
    assert(np.array_equal(game.state, expected))
    game._rotate('left', reverse=True)
    assert(np.array_equal(game.state, expected))

    # 90 rotation (up)
    game = GameState()
    state = np.array([[2, 4, 8, 16],
                      [32, 64, 128, 256],
                      [16, 4, 8, 2],
                      [256, 128, 64, 2]])
    expected = np.array([[16, 256, 2, 2],
                         [8, 128, 8, 64],
                         [4, 64, 4, 128],
                         [2, 32, 16, 256]])
    expected2 = np.copy(state)
    game.state = state
    game._rotate('up')
    assert(np.array_equal(game.state, expected))
    game._rotate('up', reverse=True)
    assert(np.array_equal(game.state, expected2))

    # 180 rotation (right)
    game = GameState()
    state = np.array([[2, 4, 8, 16],
                      [32, 64, 128, 256],
                      [16, 4, 8, 2],
                      [256, 128, 64, 2]])
    expected = np.array([[2, 64, 128, 256],
                         [2, 8, 4, 16],
                         [256, 128, 64, 32],
                         [16, 8, 4, 2]])
    expected2 = np.copy(state)
    game.state = state
    game._rotate('right')
    assert(np.array_equal(game.state, expected))
    game._rotate('right', reverse=True)
    assert(np.array_equal(game.state, expected2))

    # 270 rotation (down)
    game = GameState()
    state = np.array([[2, 4, 8, 16],
                      [32, 64, 128, 256],
                      [16, 4, 8, 2],
                      [256, 128, 64, 2]])
    expected = np.array([[256, 16, 32, 2],
                         [128, 4, 64, 4],
                         [64, 8, 128, 8],
                         [2, 2, 256, 16]])
    expected2 = np.copy(state)
    game.state = state
    game._rotate('down')
    assert(np.array_equal(game.state, expected))
    game._rotate('down', reverse=True)
    assert(np.array_equal(game.state, expected2))


def test_merge():
    # test normal
    game = GameState()
    state = np.array([[0, 0, 16, 16],
                      [0, 0, 0, 0],
                      [0, 0, 0, 0],
                      [0, 0, 0, 0]])
    expected = np.array([[0, 0, 32, 0],
                         [0, 0, 0, 0],
                         [0, 0, 0, 0],
                         [0, 0, 0, 0]])
    game.state = state
    score = game._merge()
    assert(np.array_equal(game.state, expected))
    assert(score == 32)

    # test full board
    game = GameState()
    state = np.array([[8, 8, 8, 8],
                      [8, 8, 8, 8],
                      [8, 8, 8, 8],
                      [8, 8, 8, 8]])
    expected = np.array([[16, 0, 16, 0],
                         [16, 0, 16, 0],
                         [16, 0, 16, 0],
                         [16, 0, 16, 0]])
    game.state = state
    score = game._merge()
    assert(np.array_equal(game.state, expected))
    assert(score == 128)

    # test no change
    game = GameState()
    state = np.array([[8, 16, 0, 0],
                      [0, 0, 0, 0],
                      [32, 8, 4, 2],
                      [4, 0, 0, 0]])
    expected = np.array([[8, 16, 0, 0],
                         [0, 0, 0, 0],
                         [32, 8, 4, 2],
                         [4, 0, 0, 0]])
    game.state = state
    score = game._merge()
    assert(np.array_equal(game.state, expected))
    assert(score == 0)

    # test with distanced merge
    game = GameState()
    state = np.array([[8, 0, 0, 8],
                      [8, 0, 0, 8],
                      [4, 0, 4, 2],
                      [2, 4, 0, 4]])
    expected = np.array([[16, 0, 0, 0],
                         [16, 0, 0, 0],
                         [8, 0, 0, 2],
                         [2, 8, 0, 0]])
    game.state = state
    score = game._merge()
    assert(np.array_equal(game.state, expected))
    assert(score == 48)

    # test blocked merge
    game = GameState()
    state = np.array([[8, 4, 0, 8],
                      [4, 2, 4, 0],
                      [2, 2, 2, 2],
                      [8, 2, 8, 2]])
    expected = np.array([[8, 4, 0, 8],
                         [4, 2, 4, 0],
                         [4, 0, 4, 0],
                         [8, 2, 8, 2]])
    game.state = state
    score = game._merge()
    print(game.state)
    assert(np.array_equal(game.state, expected))
    assert(score == 8)


def test_flush():
    # normal flush
    game = GameState()
    state = np.array([[2, 0, 0, 2],
                      [0, 2, 0, 2],
                      [0, 0, 2, 2],
                      [0, 0, 0, 2]])
    expected = np.array([[2, 2, 0, 0],
                         [2, 2, 0, 0],
                         [2, 2, 0, 0],
                         [2, 0, 0, 0]])
    game.state = state
    game._flush()
    assert(np.array_equal(game.state, expected))

    # more complicated
    game = GameState()
    state = np.array([[8, 4, 2, 8],
                      [2, 4, 2, 0],
                      [2, 0, 4, 2],
                      [2, 4, 0, 2]])
    expected = np.array([[8, 4, 2, 8],
                         [2, 4, 2, 0],
                         [2, 4, 2, 0],
                         [2, 4, 2, 0]])
    game.state = state
    game._flush()
    assert(np.array_equal(game.state, expected))

    # no change
    game = GameState()
    state = np.array([[8, 4, 2, 8],
                      [2, 4, 2, 2],
                      [2, 2, 4, 2],
                      [2, 4, 2, 2]])
    expected = np.array([[8, 4, 2, 8],
                         [2, 4, 2, 2],
                         [2, 2, 4, 2],
                         [2, 4, 2, 2]])
    game.state = state
    game._flush()
    assert(np.array_equal(game.state, expected))


def test_is_lost():
    # not lost with 0s
    game = GameState()
    state = np.array([[8, 4, 2, 8],
                      [2, 4, 2, 0],
                      [2, 0, 4, 2],
                      [2, 4, 0, 2]])
    game.state = state
    lost = game.is_lost()
    assert(lost is False)

    # not lost no 0s
    game = GameState()
    state = np.array([[8, 16, 4, 2],
                      [4, 2, 16, 4],
                      [128, 4, 2, 8],
                      [128, 8, 4, 2]])
    game.state = state
    lost = game.is_lost()
    assert(lost is False)

    # lost game
    game = GameState()
    state = np.array([[8, 16, 4, 2],
                      [4, 2, 16, 4],
                      [128, 4, 2, 8],
                      [2, 8, 4, 2]])
    game.state = state
    lost = game.is_lost()
    assert(lost is True)


def test_move():
    # right
    game = GameState()
    state = np.array([[8, 8, 0, 0],
                      [0, 4, 0, 0],
                      [0, 0, 0, 0],
                      [0, 0, 0, 0]])
    game.state = state
    _ = game.move('right')
    assert(game.score == 16)
    assert(game.state[0, 3] == 16)
    assert(game.state[1, 3] == 4)
    assert(np.count_nonzero(game.state == 0) == 13)

    # left
    game = GameState()
    state = np.array([[8, 8, 0, 0],
                      [0, 4, 0, 0],
                      [0, 0, 0, 0],
                      [0, 0, 0, 0]])
    game.state = state
    _ = game.move('left')
    assert(game.score == 16)
    assert(game.state[0, 0] == 16)
    assert(game.state[1, 0] == 4)
    assert(np.count_nonzero(game.state == 0) == 13)

    # up
    game = GameState()
    state = np.array([[8, 8, 0, 0],
                      [0, 4, 0, 0],
                      [8, 0, 0, 0],
                      [0, 0, 0, 0]])
    game.state = state
    _ = game.move('up')
    assert(game.score == 16)
    assert(game.state[0, 0] == 16)
    assert(game.state[1, 1] == 4)
    assert(game.state[0, 1] == 8)
    assert(np.count_nonzero(game.state == 0) == 12)

    # down
    game = GameState()
    state = np.array([[8, 8, 0, 0],
                      [0, 4, 0, 0],
                      [8, 0, 0, 0],
                      [0, 0, 0, 0]])
    game.state = state
    _ = game.move('down')
    assert(game.score == 16)
    assert(game.state[3, 0] == 16)
    assert(game.state[3, 1] == 4)
    assert(game.state[2, 1] == 8)
    assert(np.count_nonzero(game.state == 0) == 12)


def test_large_game():
    game = GameState(size=50)
    game.move('right')
    game.move('left')
    game.move('up')
    game.move('down')

def test_compact():
    game = GameState(size=4)
    state = np.array([[8, 8, 0, 0],
                      [0, 4, 0, 0],
                      [0, 0, 0, 0],
                      [0, 0, 0, 0]])
    expected = bitarray('0011001100000000000000100000000000000000000000000000000000000000')
    game.state = state
    bitarr = game.compact()
    assert(bitarr == expected)
