from numpy import random
import keyboard
import tkinter as tk

from game.game import GameState
from genetic.player import GeneticPlayer
import genetic.constants as const

class GeneticAgent():
	'''
	Uses the genetic algorithm to play the game of 2048
	'''
	def __init__(self):
		players_list = [GeneticPlayer() for _ in range(const.POPULATION_SIZE)]
		self.ranked_players = sorted(players_list,
							key=lambda x: x.fitness, 
							reverse=True)
		self.root = tk.Tk()
		self.app = Application(master=self.root, option='genetic')
		self.app.mainloop()
		self.visualize_moves(self.ranked_players[0])


	def genetic_alg(self):
		'''
		Runs the genetic algorithm for unlimited number of generations
		To stop the algorithm and visually evaluate current best, press
		the Tab key.
		To resume algorithm, press the Enter key.
		'''
		while True:
			if keyboard.is_pressed('Tab'):
				# move current best of ranked players to game window
				self.visualize_moves(self.ranked_players[0])
				keyboard.wait('Enter')
			else:
				# proceed with player mutation and mating
				


	def visualize_moves(self, player):
		'''
		Uses 2048 game window to simulate player's moves
		'''
		self.app.simulate_game(player.chromosome, game_state=player.game.initial_state)

		