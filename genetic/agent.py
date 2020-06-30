from numpy import random
import tkinter as tk

from game.window import Application
from genetic.player import GeneticPlayer
import genetic.constants as const

class GeneticAgent():
	'''
	Uses the genetic algorithm to play the game of 2048
	'''
	def __init__(self):
		players_list = [GeneticPlayer(GeneticPlayer.create_genome()).calculate_fitness() for _ in range(const.POPULATION_SIZE)]
		players_list = []
		for _ in range(const.POPULATION_SIZE):
			player = GeneticPlayer(GeneticPlayer.create_genome())
			player.calculate_fitness()
			players_list.append(player)
		self.ranked_players = sorted(players_list,
							key=lambda x: x.fitness, 
							reverse=True)
		self.visualize_moves(players_list[0])


	def genetic_alg(self):
		'''
		Runs the genetic algorithm for unlimited number of generations
		To stop the algorithm and visually evaluate current best, press
		the Tab key.
		To resume algorithm, press the Enter key.
		'''
		generation = 1
		while True:
			extend = generation % const.GEN_OFFSET == 0
			if extend:
				# move current best of ranked players to game window
				self.visualize_moves(self.ranked_players[0])
			new_gen = []
			for _ in range(const.POPULATION_SIZE):
				# pick random players and mate them
				p1 = random.choice(self.ranked_players[:500])
				p2 = random.choice(self.ranked_players[:500])
				child = p1.mate(p2)
				# extend size of chromosome for child
				if extend:
					child.extend()
				child.calculate_fitness()
				new_gen.append(child)
			# sort new players based on fitness
			self.ranked_players = sorted(new_gen,
										 key=lambda x: x.fitness,
										 reverse=True)
			generation += 1
			print(f'{generation} top ranked fitness: {self.ranked_players[0].fitness}')


	def visualize_moves(self, player):
		'''
		Uses 2048 game window to simulate player's moves
		'''
		self.root = tk.Tk()
		self.app = Application(master=self.root, option='genetic')
		self.app.after(10, self.app.simulate_game(player.chromosome, starting_board=player.initial_state))
		self.app.mainloop()

		