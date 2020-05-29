'''
Contributor(s): Thomas Hopkins

Object module for Player class
'''

from numpy import random

from game.game import GameState
from constants import *

class GeneticPlayer():
    '''
    Class for a single Player in the genetic algorithm
    '''
    def __init__(self, chromosome):
        '''
        Builds Player with input chromosome
        '''
        self.genes = GENE_POOL
        self.chromosome = chromosome
        self.fitness = 0
        self.game = GameState()
        self.outcome = ''
        self.play()

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
        gene = R_GLOBAL.choice(genes)
        return str(gene)

    def play(self):
        '''
        Driver function for starting a game of 2048
        '''
        self.game = logic.new_game()
        self.game = logic.add_new(self.game, self.random)
        self.game = logic.add_new(self.game, self.random)
        self.outcome = self.simulate()

    def perform_action(self, allele):
        '''
        Moves right, left, up, or down based on move parameter
        '''
        if allele == 'R':
            self.game = logic.right(self.game)
        elif allele == 'L':
            self.game = logic.left(self.game)
        elif allele == 'U':
            self.game = logic.up(self.game)
        elif allele == 'D':
            self.game = logic.down(self.game)

    def compare_game(self, tmp):
        '''
        Compares game to check for moves that do NOT change the board
        '''
        if tmp != self.game:
            self.game = logic.add_new(self.game, self.random)
            self.fitness = self.calculate_fitness()

    def replace(self, exclude):
        '''
        Replaces repeating characters to prevent stalling
        '''
        genes = GENE_POOL.replace(exclude, '')
        new_allele = R_GLOBAL.choice(genes)
        return new_allele

    def simulate(self):
        '''
        Simulates the play of a single game of 2048
        '''
        game_state = 'continue'
        is_repeat = False
        count = 0
        for i in range(len(self.chromosome)):
            if is_repeat:
                self.chromosome[i] = self.replace(self.chromosome[i-1])
            tmp = [x[:] for x in self.game]
            count += 1
            self.perform_action(self.chromosome[i])
            is_repeat = self.compare_game(tmp)
            game_state = logic.game_state(self.game)
            if game_state != 'continue':
                break
        return game_state

    def mate(self, other):
        '''
        Mates two Player objects together to produce one Player offspring
        '''
        child = ''
        for p1, p2 in zip(self.chromosome[:-EXTEND_SIZE], other.chromosome[:-EXTEND_SIZE]):
            prob = R_GLOBAL.random_sample()
            if prob < .5:
                child += p1
            else:
                child += p2
        for p1, p2 in zip(self.chromosome[-EXTEND_SIZE:], other.chromosome[-EXTEND_SIZE:]):
            prob = R_GLOBAL.random_sample()
            if prob < ((1.0 - MUTATION_RATE) / 2.0):
                child += p1
            elif prob < (1.0 - MUTATION_RATE):
                child += p2
            else:
                child += self.mutate()
        return Player(child)

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
        score = logic.score(self.game)
        return score
