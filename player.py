from numpy import random
import logic

class Player(object):
    def __init__(self, chromosome):
        self.genes = 'LURD'
        self.chromosome = chromosome
        self.game = logic.new_game()
        self.fitness = self.calculate_fitness()

    def mutate(self):
        gene = random.choice(self.genes)
        return gene

    def simulate(self):
        # play game
        pass

    def mate(self, other):
        # merge genes with randomness
        pass

    def calculate_fitness(self):
        score = logic.score(self.game)
        return score
