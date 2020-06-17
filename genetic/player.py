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
        self.fitness = self.calculate_fitness()

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

    def calculate_fitness(self):
        '''
        Calculates the fitness of the Player
        '''
        return 0
