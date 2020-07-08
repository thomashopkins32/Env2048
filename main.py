
import tkinter as tk
from game.window import Application
from genetic.agent import GeneticAgent
import sys


def manual_play():
	root = tk.Tk()
	app = Application(master=root, option='manual')
	app.mainloop()


if __name__ == '__main__':
	# TODO: argparse!!!
	sys.setrecursionlimit(5000)
	if len(sys.argv) == 2:
		if sys.argv[1] == 'genetic':
			agent = GeneticAgent()
			agent.genetic_alg()
		elif sys.argv[1] == 'manual':
			manual_play()
		elif sys.argv[1] == 'expectimax':
			root = tk.Tk()
			app = Application(master=root, option='expectimax')
			app.simulate_game_from_scratch()
		else:
			print("unknown argument " + sys.argv[1] + ' provided...')
			quit()
	elif len(sys.argv) == 1:
		manual_play()
	else:
		print('Too many arguments provided')