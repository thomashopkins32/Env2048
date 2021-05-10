import sys

import curses

from AI2048.game import GameState

N = int(sys.argv[1])
KEY_DICT = {'KEY_UP': 'up',
            'KEY_DOWN': 'down',
            'KEY_RIGHT': 'right',
            'KEY_LEFT': 'left'}
console = curses.initscr()
console.keypad(True)
console.clear()

def print_game(game):
    console.clear()
    for i in range(N):
        console.addstr(i, 0, str(list(game.state[i])))
    console.addstr(N, 0, f'Score: {game.score}')
    console.refresh()

game = GameState(size=N)
print_game(game)
while not game.lost:
    key = console.getkey()
    move = KEY_DICT[key]
    game.move(move)
    print_game(game)

curses.endwin()