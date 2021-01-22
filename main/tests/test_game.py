'''
Unit testing for GameState module
'''
import numpy as np

from main.game import GameState


def test_new_game():
    game = GameState()
    assert(game.state.shape == (4, 4))
    assert(np.count_nonzero(game.state == 0) == 14)
    assert(np.count_nonzero(game.state < 0) == 0)
    assert(np.count_nonzero(game.state > 0) == 2)
    assert(np.count_nonzero(game.state > 4) == 0)


def test_old_game():
    game = GameState(state=np.array([[2, 2, 2, 2],
                                     [2, 2, 2, 2],
                                     [2, 2, 2, 2],
                                     [2, 2, 2, 2]]))
    assert(game.state.shape == (4, 4))
    assert(np.count_nonzero(game.state == 2) == 16)


def test_add_tile():
    game = GameState(state=np.array([[0, 0, 0, 0],
                                     [0, 0, 0, 0],
                                     [0, 0, 0, 0],
                                     [0, 0, 0, 0]]))
    new_state = game._add_tile(game.state)
    assert(np.count_nonzero(new_state == 0) == 15)
    assert(np.count_nonzero(new_state > 4) == 0)
    assert(np.count_nonzero(new_state < 0) == 0)
    two_count = np.count_nonzero(new_state == 2)
    four_count = np.count_nonzero(new_state == 4)
    assert((two_count == 0 and four_count == 1) or
           (two_count == 1 and four_count == 0))


def test_rotate():
    # no rotation (left)
    game = GameState(state=np.array([[2, 4, 8, 16],
                                     [32, 64, 128, 256],
                                     [16, 4, 8, 2],
                                     [256, 128, 64, 2]]))
    expected = np.array([[2, 4, 8, 16],
                         [32, 64, 128, 256],
                         [16, 4, 8, 2],
                         [256, 128, 64, 2]])
    game_t = game._rotate(game.state, 'left')
    assert(np.array_equal(game_t, expected))
    game_t = game._rotate(game_t, 'left', reverse=True)
    assert(np.array_equal(game_t, expected))

    # 90 rotation (up)
    game = GameState(state=np.array([[2, 4, 8, 16],
                                     [32, 64, 128, 256],
                                     [16, 4, 8, 2],
                                     [256, 128, 64, 2]]))
    expected = np.array([[16, 256, 2, 2],
                         [8, 128, 8, 64],
                         [4, 64, 4, 128],
                         [2, 32, 16, 256]])
    game_t = game._rotate(game.state, 'up')
    assert(np.array_equal(game_t, expected))
    game_t = game._rotate(game_t, 'up', reverse=True)
    assert(np.array_equal(game_t, game.state))

    # 180 rotation (right)
    game = GameState(state=np.array([[2, 4, 8, 16],
                                     [32, 64, 128, 256],
                                     [16, 4, 8, 2],
                                     [256, 128, 64, 2]]))
    expected = np.array([[2, 64, 128, 256],
                         [2, 8, 4, 16],
                         [256, 128, 64, 32],
                         [16, 8, 4, 2]])
    game_t = game._rotate(game.state, 'right')
    assert(np.array_equal(game_t, expected))
    game_t = game._rotate(game_t, 'right', reverse=True)
    assert(np.array_equal(game_t, game.state))

    # 270 rotation (down)
    game = GameState(state=np.array([[2, 4, 8, 16],
                                     [32, 64, 128, 256],
                                     [16, 4, 8, 2],
                                     [256, 128, 64, 2]]))
    expected = np.array([[256, 16, 32, 2],
                         [128, 4, 64, 4],
                         [64, 8, 128, 8],
                         [2, 2, 256, 16]])
    game_t = game._rotate(game.state, 'down')
    assert(np.array_equal(game_t, expected))
    game_t = game._rotate(game_t, 'down', reverse=True)
    assert(np.array_equal(game_t, game.state))


def test_merge():
    # test normal
    game = GameState(state=np.array([[0, 0, 16, 16],
                                     [0, 0, 0, 0],
                                     [0, 0, 0, 0],
                                     [0, 0, 0, 0]]))
    expected = np.array([[0, 0, 32, 0],
                         [0, 0, 0, 0],
                         [0, 0, 0, 0],
                         [0, 0, 0, 0]])
    game_t, score = game._merge(game.state)
    assert(np.array_equal(game_t, expected))
    assert(score == 32)

    # test full board
    game = GameState(state=np.array([[8, 8, 8, 8],
                                     [8, 8, 8, 8],
                                     [8, 8, 8, 8],
                                     [8, 8, 8, 8]]))
    expected = np.array([[16, 0, 16, 0],
                         [16, 0, 16, 0],
                         [16, 0, 16, 0],
                         [16, 0, 16, 0]])
    game_t, score = game._merge(game.state)
    assert(np.array_equal(game_t, expected))
    assert(score == 128)

    # test no change
    game = GameState(state=np.array([[8, 16, 0, 0],
                                     [0, 0, 0, 0],
                                     [32, 8, 4, 2],
                                     [4, 0, 0, 0]]))
    expected = np.array([[8, 16, 0, 0],
                         [0, 0, 0, 0],
                         [32, 8, 4, 2],
                         [4, 0, 0, 0]])
    game_t, score = game._merge(game.state)
    assert(np.array_equal(game_t, expected))
    assert(score == 0)

    # test with distanced merge
    game = GameState(state=np.array([[8, 0, 0, 8],
                                     [8, 0, 0, 8],
                                     [4, 0, 4, 2],
                                     [2, 4, 0, 4]]))
    expected = np.array([[16, 0, 0, 0],
                         [16, 0, 0, 0],
                         [8, 0, 0, 2],
                         [2, 8, 0, 0]])
    game_t, score = game._merge(game.state)
    assert(np.array_equal(game_t, expected))
    assert(score == 48)


def test_flush():
    # normal flush
    game = GameState(state=np.array([[2, 0, 0, 2],
                                     [0, 2, 0, 2],
                                     [0, 0, 2, 2],
                                     [0, 0, 0, 2]]))
    expected = np.array([[2, 2, 0, 0],
                         [2, 2, 0, 0],
                         [2, 2, 0, 0],
                         [2, 0, 0, 0]])
    game_t = game._flush(game.state)
    assert(np.array_equal(game_t, expected))

    # more complicated
    game = GameState(state=np.array([[8, 4, 2, 8],
                                     [2, 4, 2, 0],
                                     [2, 0, 4, 2],
                                     [2, 4, 0, 2]]))
    expected = np.array([[8, 4, 2, 8],
                         [2, 4, 2, 0],
                         [2, 4, 2, 0],
                         [2, 4, 2, 0]])
    game_t = game._flush(game.state)
    assert(np.array_equal(game_t, expected))

    # no change
    game = GameState(state=np.array([[8, 4, 2, 8],
                                     [2, 4, 2, 2],
                                     [2, 2, 4, 2],
                                     [2, 4, 2, 2]]))
    expected = np.array([[8, 4, 2, 8],
                         [2, 4, 2, 2],
                         [2, 2, 4, 2],
                         [2, 4, 2, 2]])
    game_t = game._flush(game.state)
    assert(np.array_equal(game_t, expected))


def test_is_lost():
    # not lost with 0s
    game = GameState(state=np.array([[8, 4, 2, 8],
                                     [2, 4, 2, 0],
                                     [2, 0, 4, 2],
                                     [2, 4, 0, 2]]))
    lost = game.is_lost()
    assert(lost is False)

    # not lost no 0s
    game = GameState(state=np.array([[8, 16, 4, 2],
                                     [4, 2, 16, 4],
                                     [128, 4, 2, 8],
                                     [128, 8, 4, 2]]))
    lost = game.is_lost()
    assert(lost is False)

    # lost game
    game = GameState(state=np.array([[8, 16, 4, 2],
                                     [4, 2, 16, 4],
                                     [128, 4, 2, 8],
                                     [2, 8, 4, 2]]))
    lost = game.is_lost()
    assert(lost is True)


def test_move():
    # right
    game = GameState(state=np.array([[8, 8, 0, 0],
                                     [0, 4, 0, 0],
                                     [0, 0, 0, 0],
                                     [0, 0, 0, 0]]))
    game_t = game.move('right')
    assert(game_t.score == 16)
    assert(game_t.state[0, 3] == 16)
    assert(game_t.state[1, 3] == 4)
    assert(np.count_nonzero(game_t.state == 0) == 13)

    # left
    game = GameState(state=np.array([[8, 8, 0, 0],
                                     [0, 4, 0, 0],
                                     [0, 0, 0, 0],
                                     [0, 0, 0, 0]]))
    game_t = game.move('left')
    assert(game_t.score == 16)
    assert(game_t.state[0, 0] == 16)
    assert(game_t.state[1, 0] == 4)
    assert(np.count_nonzero(game_t.state == 0) == 13)

    # up
    game = GameState(state=np.array([[8, 8, 0, 0],
                                     [0, 4, 0, 0],
                                     [8, 0, 0, 0],
                                     [0, 0, 0, 0]]))
    game_t = game.move('up')
    assert(game_t.score == 16)
    assert(game_t.state[0, 0] == 16)
    assert(game_t.state[1, 1] == 4)
    assert(game_t.state[0, 1] == 8)
    assert(np.count_nonzero(game_t.state == 0) == 12)

    # down
    game = GameState(state=np.array([[8, 8, 0, 0],
                                     [0, 4, 0, 0],
                                     [8, 0, 0, 0],
                                     [0, 0, 0, 0]]))
    game_t = game.move('down')
    assert(game_t.score == 16)
    assert(game_t.state[3, 0] == 16)
    assert(game_t.state[3, 1] == 4)
    assert(game_t.state[2, 1] == 8)
    assert(np.count_nonzero(game_t.state == 0) == 12)
