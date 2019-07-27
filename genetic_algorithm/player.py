from numpy import random
import logic
from constants import *

# Class for AI
class Player(object):
    # constructor
    def __init__(self, chromosome):
        self.genes = GENE_POOL
        self.chromosome = chromosome
        self.fitness = 0
        self.game = []
        self.outcome = ''
        self.random = random.RandomState(41)
        self.play()

    # creates the initial moves at random
    @classmethod
    def create_genome(self):
        chromosome = ''
        for i in range(EXTEND_SIZE):
            chromosome += self.mutate()
        return chromosome

    # randomly selects a move to make
    @classmethod
    def mutate(self):
        genes = [i for i in GENE_POOL]
        gene = R_GLOBAL.choice(genes)
        return str(gene)

    # driver function for playing 2048
    def play(self):
        self.game = logic.new_game()
        self.game = logic.add_new(self.game, self.random)
        self.game = logic.add_new(self.game, self.random)
        self.outcome = self.simulate()

    # moves right, left, up, or down based on move parameter
    def perform_action(self, allele):
        if allele == 'R':
            self.game = logic.right(self.game)
        elif allele == 'L':
            self.game = logic.left(self.game)
        elif allele == 'U':
            self.game = logic.up(self.game)
        elif allele == 'D':
            self.game = logic.down(self.game)

    # compares game to check for moves that dont change the board
    def compare_game(self, tmp):
        if tmp != self.game:
            self.game = logic.add_new(self.game, self.random)
            self.fitness = self.calculate_fitness()

    # replaces repeating characters to prevent stalling
    def replace(self, exclude):
        genes = GENE_POOL.replace(exclude, '')
        new_allele = R_GLOBAL.choice(genes)
        return new_allele

    # simulates the play of a single game of 2048
    def simulate(self):
        game_state = 'continue'
        is_repeat = False
        count = 0
        for i in range(len(self.chromosome)):
            if is_repeat:
                self.chromsome[i] = self.replace(self.chromsome[i-1])
            tmp = [x[:] for x in self.game]
            count += 1
            self.perform_action(self.chromosome[i])
            is_repeat = self.compare_game(tmp)
            game_state = logic.game_state(self.game)
            if game_state != 'continue':
                break
        return game_state

    # mates two Player objects together to produce offspring
    def mate(self, other):
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

    # prints useful info for Player object
    def debug(self):
        print('Fitness: ' + str(self.fitness))
        print('Game: ')
        print(self.game)
        print('Chromosome: ' + self.chromosome)

    # extends the moveset of Player
    def extend(self):
        for i in range(EXTEND_SIZE):
            self.chromosome += self.mutate()

    # calculates the fitness of a Player
    def calculate_fitness(self):
        score = logic.score(self.game)
        return score
