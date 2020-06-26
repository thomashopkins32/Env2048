'''
Contributor(s): Thomas Hopkins

Object module for Player class
'''

from numpy import random

from game.game import GameState
from genetic.constants import *

class GeneticPlayer():
    '''
    Class for a single Player in the genetic algorithm
    '''
    def __init__(self, chromosome):
        '''
        Builds Player with input chromosome
        '''
        self.chromosome = chromosome
        self.game = GameState()
        self.initial_state = self.game.get_board()
        self.game.perform_multiple_actions(chromosome)
        self.fitness = 0

    @classmethod
    def create_genome(cls):
        '''
        Creates the initial moves at random
        '''
        chromosome = ''
        for _ in range(EXTEND_SIZE):
            chromosome += cls.mutate()
        return chromosome

    @classmethod
    def mutate(cls):
        '''
        Randomly selects a move to make
        '''
        genes = [i for i in GENE_POOL]
        gene = random.choice(genes)
        return str(gene)

    def replace(self, exclude):
        '''
        Replaces repeating characters to prevent stalling
        '''
        genes = GENE_POOL.replace(exclude, '')
        new_allele = random.choice(genes)
        return new_allele

    def mate(self, other):
        '''
        Mates two Player objects together to produce one Player offspring
        '''
        child = ''
        for p1, p2 in zip(self.chromosome[:-EXTEND_SIZE], other.chromosome[:-EXTEND_SIZE]):
            prob = random.random_sample()
            if prob < .5:
                child += p1
            else:
                child += p2
        for p1, p2 in zip(self.chromosome[-EXTEND_SIZE:], other.chromosome[-EXTEND_SIZE:]):
            prob = random.random_sample()
            if prob < ((1.0 - MUTATION_RATE) / 2.0):
                child += p1
            elif prob < (1.0 - MUTATION_RATE):
                child += p2
            else:
                child += self.mutate()
        return GeneticPlayer(child)

    def debug(self):
        '''
        Prints useful info for Player object to the console
        '''
        print('Fitness: ' + str(self.fitness))
        print('Game: ')
        print(self.game)
        print('Chromosome: ' + self.chromosome)

    def extend(self):
        '''
        Extends the moveset of the Player
        '''
        for _ in range(EXTEND_SIZE):
            self.chromosome += self.mutate()
        self.fitness = self.calculate_fitness()

    def calculate_fitness(self):
        '''
        Calculates the fitness of the Player
        '''
        if self.game.lost:
            self.fitness = 0
            return
        board = self.game.matrix
        position_heuristic = 0
        for i in range(4):
            for j in range(4):
                position_heuristic += board[i][j] * POSITION_TABLE[i][j]
        difference_penalty = 0
        for i in range(4):
            for j in range(4):
                neighbors = [(i+1, j), (i-1, j), (i, j+1), (i, j-1)]
                for (ni, nj) in neighbors:
                    if ni < 0 or ni >= 4 or nj < 0 or nj >= 4:
                        continue
                    difference_penalty += abs(board[i][j] - board[ni][nj])
        difference_penalty = -difference_penalty
        increasing_along_edge = 0
        bottom_edge = sorted(board[3])
        if bottom_edge == board[3]:
            increasing_along_edge += 100
        right_edge = sorted(board[:][3])
        if right_edge == board[:][3]:
            increasing_along_edge += 100
        self.fitness = 5*position_heuristic + 1*difference_penalty + 5*increasing_along_edge
