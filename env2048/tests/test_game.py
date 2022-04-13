'''
Unit testing for envState module
'''
import numpy as np

from AI2048.env import Env2048


def test_new_env():
    env = Env2048()
    o = env.reset()
    assert(o.shape == (4, 4))
    assert(np.count_nonzero(o == 0) == 14)
    assert(np.count_nonzero(o < 0) == 0)
    assert(np.count_nonzero(o > 0) == 2)
    assert(np.count_nonzero(o > 4) == 0)


def test_old_env():
    env = Env2048()
    env.reset()
    state = np.array([[2, 2, 2, 2],
                      [2, 2, 2, 2],
                      [2, 2, 2, 2],
                      [2, 2, 2, 2]])
    env._state = state
    assert(env._state.shape == (4, 4))
    assert(np.count_nonzero(env._state == 2) == 16)


def test_add_tile():
    env = Env2048()
    env.reset()
    state = np.array([[0, 0, 0, 0],
                      [0, 0, 0, 0],
                      [0, 0, 0, 0],
                      [0, 0, 0, 0]])
    env._state = state
    env._add_tile()
    assert(np.count_nonzero(env._state == 0) == 15)
    assert(np.count_nonzero(env._state > 4) == 0)
    assert(np.count_nonzero(env._state < 0) == 0)
    two_count = np.count_nonzero(env._state == 2)
    four_count = np.count_nonzero(env._state == 4)
    assert((two_count == 0 and four_count == 1) or
           (two_count == 1 and four_count == 0))


def test_rotate():
    # no rotation (left)
    env = Env2048()
    env.reset()
    state = np.array([[2, 4, 8, 16],
                      [32, 64, 128, 256],
                      [16, 4, 8, 2],
                      [256, 128, 64, 2]])
    expected = np.array([[2, 4, 8, 16],
                         [32, 64, 128, 256],
                         [16, 4, 8, 2],
                         [256, 128, 64, 2]])
    env._state = state
    env._rotate(0)
    assert(np.array_equal(env._state, expected))
    env._rotate(0, reverse=True)
    assert(np.array_equal(env._state, expected))

    # 90 rotation (up)
    env.reset()
    state = np.array([[2, 4, 8, 16],
                      [32, 64, 128, 256],
                      [16, 4, 8, 2],
                      [256, 128, 64, 2]])
    expected = np.array([[16, 256, 2, 2],
                         [8, 128, 8, 64],
                         [4, 64, 4, 128],
                         [2, 32, 16, 256]])
    expected2 = np.copy(state)
    env._state = state
    env._rotate(1)
    assert(np.array_equal(env._state, expected))
    env._rotate(1, reverse=True)
    assert(np.array_equal(env._state, expected2))

    # 180 rotation (right)
    env.reset()
    state = np.array([[2, 4, 8, 16],
                      [32, 64, 128, 256],
                      [16, 4, 8, 2],
                      [256, 128, 64, 2]])
    expected = np.array([[2, 64, 128, 256],
                         [2, 8, 4, 16],
                         [256, 128, 64, 32],
                         [16, 8, 4, 2]])
    expected2 = np.copy(state)
    env._state = state
    env._rotate(2)
    assert(np.array_equal(env._state, expected))
    env._rotate(2, reverse=True)
    assert(np.array_equal(env._state, expected2))

    # 270 rotation (down)
    env.reset()
    state = np.array([[2, 4, 8, 16],
                      [32, 64, 128, 256],
                      [16, 4, 8, 2],
                      [256, 128, 64, 2]])
    expected = np.array([[256, 16, 32, 2],
                         [128, 4, 64, 4],
                         [64, 8, 128, 8],
                         [2, 2, 256, 16]])
    expected2 = np.copy(state)
    env._state = state
    env._rotate(3)
    assert(np.array_equal(env._state, expected))
    env._rotate(3, reverse=True)
    assert(np.array_equal(env._state, expected2))


def test_merge():
    # test normal
    env = Env2048()
    env.reset()
    state = np.array([[0, 0, 16, 16],
                      [0, 0, 0, 0],
                      [0, 0, 0, 0],
                      [0, 0, 0, 0]])
    expected = np.array([[0, 0, 32, 0],
                         [0, 0, 0, 0],
                         [0, 0, 0, 0],
                         [0, 0, 0, 0]])
    env._state = state
    score = env._merge()
    assert(np.array_equal(env._state, expected))
    assert(score == 32)

    # test full board
    env.reset()
    state = np.array([[8, 8, 8, 8],
                      [8, 8, 8, 8],
                      [8, 8, 8, 8],
                      [8, 8, 8, 8]])
    expected = np.array([[16, 0, 16, 0],
                         [16, 0, 16, 0],
                         [16, 0, 16, 0],
                         [16, 0, 16, 0]])
    env._state = state
    score = env._merge()
    assert(np.array_equal(env._state, expected))
    assert(score == 128)

    # test no change
    env.reset()
    state = np.array([[8, 16, 0, 0],
                      [0, 0, 0, 0],
                      [32, 8, 4, 2],
                      [4, 0, 0, 0]])
    expected = np.array([[8, 16, 0, 0],
                         [0, 0, 0, 0],
                         [32, 8, 4, 2],
                         [4, 0, 0, 0]])
    env._state = state
    score = env._merge()
    assert(np.array_equal(env._state, expected))
    assert(score == 0)

    # test with distanced merge
    env.reset()
    state = np.array([[8, 0, 0, 8],
                      [8, 0, 0, 8],
                      [4, 0, 4, 2],
                      [2, 4, 0, 4]])
    expected = np.array([[16, 0, 0, 0],
                         [16, 0, 0, 0],
                         [8, 0, 0, 2],
                         [2, 8, 0, 0]])
    env._state = state
    score = env._merge()
    assert(np.array_equal(env._state, expected))
    assert(score == 48)

    # test blocked merge
    env.reset()
    state = np.array([[8, 4, 0, 8],
                      [4, 2, 4, 0],
                      [2, 2, 2, 2],
                      [8, 2, 8, 2]])
    expected = np.array([[8, 4, 0, 8],
                         [4, 2, 4, 0],
                         [4, 0, 4, 0],
                         [8, 2, 8, 2]])
    env._state = state
    score = env._merge()
    assert(np.array_equal(env._state, expected))
    assert(score == 8)


def test_flush():
    # normal flush
    env = Env2048()
    env.reset()
    state = np.array([[2, 0, 0, 2],
                      [0, 2, 0, 2],
                      [0, 0, 2, 2],
                      [0, 0, 0, 2]])
    expected = np.array([[2, 2, 0, 0],
                         [2, 2, 0, 0],
                         [2, 2, 0, 0],
                         [2, 0, 0, 0]])
    env._state = state
    env._flush()
    assert(np.array_equal(env._state, expected))

    # more complicated
    env.reset()
    state = np.array([[8, 4, 2, 8],
                      [2, 4, 2, 0],
                      [2, 0, 4, 2],
                      [2, 4, 0, 2]])
    expected = np.array([[8, 4, 2, 8],
                         [2, 4, 2, 0],
                         [2, 4, 2, 0],
                         [2, 4, 2, 0]])
    env._state = state
    env._flush()
    assert(np.array_equal(env._state, expected))

    # no change
    env.reset()
    state = np.array([[8, 4, 2, 8],
                      [2, 4, 2, 2],
                      [2, 2, 4, 2],
                      [2, 4, 2, 2]])
    expected = np.array([[8, 4, 2, 8],
                         [2, 4, 2, 2],
                         [2, 2, 4, 2],
                         [2, 4, 2, 2]])
    env._state = state
    env._flush()
    assert(np.array_equal(env._state, expected))


def test_is_lost():
    # not lost with 0s
    env = Env2048()
    env.reset()
    state = np.array([[8, 4, 2, 8],
                      [2, 4, 2, 0],
                      [2, 0, 4, 2],
                      [2, 4, 0, 2]])
    env._state = state
    lost = env._is_lost()
    assert(lost is False)

    # not lost no 0s
    env.reset()
    state = np.array([[8, 16, 4, 2],
                      [4, 2, 16, 4],
                      [128, 4, 2, 8],
                      [128, 8, 4, 2]])
    env._state = state
    lost = env._is_lost()
    assert(lost is False)

    # lost env
    env.reset()
    state = np.array([[8, 16, 4, 2],
                      [4, 2, 16, 4],
                      [128, 4, 2, 8],
                      [2, 8, 4, 2]])
    env._state = state
    lost = env._is_lost()
    assert(lost is True)


def test_move():
    # right
    env = Env2048()
    env.reset()
    state = np.array([[8, 8, 0, 0],
                      [0, 4, 0, 0],
                      [0, 0, 0, 0],
                      [0, 0, 0, 0]])
    env._state = state
    _ = env.step(2)
    assert(env.score == 16)
    assert(env._state[0, 3] == 16)
    assert(env._state[1, 3] == 4)
    assert(np.count_nonzero(env._state == 0) == 13)

    # left
    env.reset()
    state = np.array([[8, 8, 0, 0],
                      [0, 4, 0, 0],
                      [0, 0, 0, 0],
                      [0, 0, 0, 0]])
    env._state = state
    _ = env.step(0)
    assert(env.score == 16)
    assert(env._state[0, 0] == 16)
    assert(env._state[1, 0] == 4)
    assert(np.count_nonzero(env._state == 0) == 13)

    # up
    env.reset()
    state = np.array([[8, 8, 0, 0],
                      [0, 4, 0, 0],
                      [8, 0, 0, 0],
                      [0, 0, 0, 0]])
    env._state = state
    _ = env.step(1)
    assert(env.score == 16)
    assert(env._state[0, 0] == 16)
    assert(env._state[1, 1] == 4)
    assert(env._state[0, 1] == 8)
    assert(np.count_nonzero(env._state == 0) == 12)

    # down
    env.reset()
    state = np.array([[8, 8, 0, 0],
                      [0, 4, 0, 0],
                      [8, 0, 0, 0],
                      [0, 0, 0, 0]])
    env._state = state
    _ = env.step(3)
    assert(env.score == 16)
    assert(env._state[3, 0] == 16)
    assert(env._state[3, 1] == 4)
    assert(env._state[2, 1] == 8)
    assert(np.count_nonzero(env._state == 0) == 12)


def test_large_env():
    env = Env2048(size=50)
    env.reset()
    env.step(0)
    env.step(1)
    env.step(2)
    env.step(3)
