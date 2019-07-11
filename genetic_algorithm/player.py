from numpy import random
import logic
from constants import *

class Player(object):
    def __init__(self, chromosome):
        self.genes = GENE_POOL
        self.chromosome = chromosome
        self.fitness = 0
        self.game = []
        self.outcome = ''
        self.random = random.RandomState(41)
        self.play()

    @classmethod
    def create_genome(self):
        chromosome = ''
        for i in range(EXTEND_SIZE):
            chromosome += self.mutate()
        return chromosome

    @classmethod
    def mutate(self):
        genes = [i for i in GENE_POOL]
        gene = R_GLOBAL.choice(genes)
        return str(gene)

    def play(self):
        self.game = logic.new_game()
        self.game = logic.add_new(self.game, self.random)
        self.game = logic.add_new(self.game, self.random)
        self.outcome = self.simulate()

    def perform_action(self, allele):
        if allele == 'R':
            self.game = logic.right(self.game)
        elif allele == 'L':
            self.game = logic.left(self.game)
        elif allele == 'U':
            self.game = logic.up(self.game)
        elif allele == 'D':
            self.game = logic.down(self.game)

    def compare_game(self, tmp):
        if tmp != self.game:
            self.game = logic.add_new(self.game, self.random)
            self.fitness = self.calculate_fitness()

    def replace(self, exclude):
        genes = GENE_POOL.replace(exclude, '')
        new_allele = R_GLOBAL.choice(genes)
        return new_allele

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

    def mate(self, other):
        child = ''
        for p1, p2 in zip(self.chromosome, other.chromosome):
            prob = R_GLOBAL.random_sample()
            if prob < ((1.0 - MUTATION_RATE) / 2.0):
                child += p1
            elif prob < (1.0 - MUTATION_RATE):
                child += p2
            else:
                child += self.mutate()
        return Player(child)

    def debug(self):
        print('Fitness: ' + str(self.fitness))
        print('Game: ')
        print(self.game)
        print('Chromosome: ' + self.chromosome)

    def extend(self):
        for i in range(EXTEND_SIZE):
            self.chromosome += self.mutate()


    def calculate_fitness(self):
        score = logic.score(self.game)
        return score
