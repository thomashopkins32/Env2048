'''
Unit testing for GameState module
'''
import numpy as np

from main.game import GameState


def test_new_game():
    game = GameState()
    assert(game.state.shape == (4,4))
    assert(np.count_nonzero(game.state == 0) == 14)
    assert(np.count_nonzero(game.state < 0) == 0)
    assert(np.count_nonzero(game.state > 0) == 2)
    assert(np.count_nonzero(game.state > 4) == 0)


def test_old_game():
    game = GameState(state=np.array([[2, 2, 2, 2],
                                     [2, 2, 2, 2],
                                     [2, 2, 2, 2],
                                     [2, 2, 2, 2]]))
    assert(game.state.shape == (4,4))
    assert(np.count_nonzero(game.state == 2) == 16)


def test_right():
    # test normal
    game = GameState(state=np.array([[0, 0, 16, 16],
                                     [0, 0, 0, 0],
                                     [0, 0, 0, 0],
                                     [0, 0, 0, 0]]))
    expected = np.array([[0, 0, 0, 32],
                         [0, 0, 0, 0],
                         [0, 0, 0, 0],
                         [0, 0, 0, 0]])
    game_r = game.merge(game.state, 'right')
    assert(np.array_equal(game_r, expected))

    # test full board
    game = GameState(state=np.array([[8, 8, 8, 8],
                                     [8, 8, 8, 8],
                                     [8, 8, 8, 8],
                                     [8, 8, 8, 8]]))
    expected = np.array([[0, 0, 16, 16],
                         [0, 0, 16, 16],
                         [0, 0, 16, 16],
                         [0, 0, 16, 16]])
    game_r = game.merge(game.state, 'right')
    assert(np.array_equal(game_r, expected))

    # test no change
    game = GameState(state=np.array([[0, 0, 8, 16],
                                     [0, 0, 0, 0],
                                     [32, 8, 4, 2],
                                     [0, 0, 0, 4]]))
    expected = np.array([[0, 0, 8, 16],
                         [0, 0, 0, 0],
                         [32, 8, 4, 2],
                         [0, 0, 0, 4]])
    game_r = game.merge(game.state, 'right')
    assert(np.array_equal(game_r, expected))

    # test with distanced merge
    game = GameState(state=np.array([[8, 0, 0, 8],
                                     [8, 0, 0, 8],
                                     [4, 0, 4, 2],
                                     [2, 4, 0, 4]]))
    expected = np.array([[0, 0, 0, 16],
                         [0, 0, 0, 16],
                         [0, 0, 8, 2],
                         [0, 0, 2, 8]])
    game_r = game.merge(game.state, 'right')
    assert(np.array_equal(game_r, expected))

    # test with blocker 
    game = GameState(state=np.array([[8, 4, 2, 8],
                                     [2, 4, 2, 0],
                                     [2, 0, 4, 2],
                                     [2, 4, 0, 2]]))
    expected = np.array([[8, 4, 2, 8],
                         [0, 2, 4, 2],
                         [0, 2, 4, 2],
                         [0, 2, 4, 2]])
    game_r = game.merge(game.state, 'right')
    assert(np.array_equal(game_r, expected))


def test_left():
    # test normal
    game = GameState(state=np.array([[0, 0, 16, 16],
                                     [0, 0, 0, 0],
                                     [0, 0, 0, 0],
                                     [0, 0, 0, 0]]))
    expected = np.array([[32, 0, 0, 0],
                         [0, 0, 0, 0],
                         [0, 0, 0, 0],
                         [0, 0, 0, 0]])
    game_r = game.merge(game.state, 'left')
    assert(np.array_equal(game_r, expected))

    # test full board
    game = GameState(state=np.array([[8, 8, 8, 8],
                                     [8, 8, 8, 8],
                                     [8, 8, 8, 8],
                                     [8, 8, 8, 8]]))
    expected = np.array([[16, 16, 0, 0],
                         [16, 16, 0, 0],
                         [16, 16, 0, 0],
                         [16, 16, 0, 0]])
    game_r = game.merge(game.state, 'left')
    assert(np.array_equal(game_r, expected))

    # test no change
    game = GameState(state=np.array([[8, 16, 0, 0],
                                     [0, 0, 0, 0],
                                     [32, 8, 4, 2],
                                     [4, 0, 0, 0]]))
    expected = np.array([[8, 16, 0, 0],
                         [0, 0, 0, 0],
                         [32, 8, 4, 2],
                         [4, 0, 0, 0]])
    game_r = game.merge(game.state, 'left')
    assert(np.array_equal(game_r, expected))

    # test with distanced merge
    game = GameState(state=np.array([[8, 0, 0, 8],
                                     [8, 0, 0, 8],
                                     [4, 0, 4, 2],
                                     [2, 4, 0, 4]]))
    expected = np.array([[16, 0, 0, 0],
                         [16, 0, 0, 0],
                         [8, 2, 0, 0],
                         [2, 8, 0, 0]])
    game_r = game.merge(game.state, 'left')
    assert(np.array_equal(game_r, expected))

    # test with blocker 
    game = GameState(state=np.array([[8, 4, 2, 8],
                                     [2, 4, 2, 0],
                                     [2, 0, 4, 2],
                                     [2, 4, 0, 2]]))
    expected = np.array([[8, 4, 2, 8],
                         [2, 4, 2, 0],
                         [2, 4, 2, 0],
                         [2, 4, 2, 0]])
    game_r = game.merge(game.state, 'left')
    assert(np.array_equal(game_r, expected))


def test_up():
    # test normal
    game = GameState(state=np.array([[0, 0, 0, 16],
                                     [0, 0, 0, 16],
                                     [0, 0, 0, 0],
                                     [0, 0, 0, 0]]))
    expected = np.array([[0, 0, 0, 32],
                         [0, 0, 0, 0],
                         [0, 0, 0, 0],
                         [0, 0, 0, 0]])
    game_r = game.merge(game.state, 'up')
    assert(np.array_equal(game_r, expected))

    # test full board
    game = GameState(state=np.array([[8, 8, 8, 8],
                                     [8, 8, 8, 8],
                                     [8, 8, 8, 8],
                                     [8, 8, 8, 8]]))
    expected = np.array([[16, 16, 16, 16],
                         [16, 16, 16, 16],
                         [0, 0, 0, 0],
                         [0, 0, 0, 0]])
    game_r = game.merge(game.state, 'up')
    assert(np.array_equal(game_r, expected))

    # test no change
    game = GameState(state=np.array([[32, 8, 8, 16],
                                     [0, 0, 4, 2],
                                     [0, 0, 0, 4],
                                     [0, 0, 0, 0]]))
    expected = np.array([[32, 8, 8, 16],
                         [0, 0, 4, 2],
                         [0, 0, 0, 4],
                         [0, 0, 0, 0]])
    game_r = game.merge(game.state, 'up')
    assert(np.array_equal(game_r, expected))

    # test with distanced merge
    game = GameState(state=np.array([[8, 8, 4, 2],
                                     [0, 0, 0, 4],
                                     [0, 0, 4, 0],
                                     [8, 8, 2, 4]]))
    expected = np.array([[16, 16, 8, 2],
                         [0, 0, 2, 8],
                         [0, 0, 0, 0],
                         [0, 0, 0, 0]])
    game_r = game.merge(game.state, 'up')
    assert(np.array_equal(game_r, expected))

    # test with blocker 
    game = GameState(state=np.array([[8, 4, 0, 4],
                                     [4, 2, 4, 0],
                                     [2, 0, 2, 2],
                                     [8, 4, 4, 4]]))
    expected = np.array([[8, 4, 4, 4],
                         [4, 2, 2, 2],
                         [2, 4, 4, 4],
                         [8, 0, 0, 0]])
    game_r = game.merge(game.state, 'up')
    assert(np.array_equal(game_r, expected))


def test_down(): 
    # test normal
    game = GameState(state=np.array([[0, 0, 0, 16],
                                     [0, 0, 0, 16],
                                     [0, 0, 0, 0],
                                     [0, 0, 0, 0]]))
    expected = np.array([[0, 0, 0, 0],
                         [0, 0, 0, 0],
                         [0, 0, 0, 0],
                         [0, 0, 0, 32]])
    game_r = game.merge(game.state, 'down')
    assert(np.array_equal(game_r, expected))

    # test full board
    game = GameState(state=np.array([[8, 8, 8, 8],
                                     [8, 8, 8, 8],
                                     [8, 8, 8, 8],
                                     [8, 8, 8, 8]]))
    expected = np.array([[0, 0, 0, 0],
                         [0, 0, 0, 0],
                         [16, 16, 16, 16],
                         [16, 16, 16, 16]])
    game_r = game.merge(game.state, 'down')
    assert(np.array_equal(game_r, expected))

    # test no change
    game = GameState(state=np.array([[0, 0, 0, 0],
                                     [0, 0, 0, 16],
                                     [0, 0, 4, 2],
                                     [32, 8, 8, 4]]))
    expected = np.array([[0, 0, 0, 0],
                         [0, 0, 0, 16],
                         [0, 0, 4, 2],
                         [32, 8, 8, 4]])
    game_r = game.merge(game.state, 'down')
    assert(np.array_equal(game_r, expected))

    # test with distanced merge
    game = GameState(state=np.array([[8, 8, 4, 2],
                                     [0, 0, 0, 4],
                                     [0, 0, 4, 0],
                                     [8, 8, 2, 4]]))
    expected = np.array([[0, 0, 0, 0],
                         [0, 0, 0, 0],
                         [0, 0, 8, 2],
                         [16, 16, 2, 8]])
    game_r = game.merge(game.state, 'down')
    assert(np.array_equal(game_r, expected))

    # test with blocker 
    game = GameState(state=np.array([[8, 4, 0, 4],
                                     [4, 2, 4, 0],
                                     [2, 0, 2, 2],
                                     [8, 4, 4, 4]]))
    expected = np.array([[8, 0, 0, 0],
                         [4, 4, 4, 4],
                         [2, 2, 2, 2],
                         [8, 4, 4, 4]])
    game_r = game.merge(game.state, 'down')
    assert(np.array_equal(game_r, expected))



def test_score():
    pass

