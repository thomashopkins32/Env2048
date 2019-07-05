from numpy import random
import logic

class Player(object):
    def __init__(self, chromosome):
        self.genes = 'LURD'
        self.chromosome = chromosome
        self.fitness = 0
        self.game = logic.new_game()
        self.game = logic.add_new(self.game)
        self.game = logic.add_new(self.game)
        self.outcome = self.simulate()

    @classmethod
    def mutate(self):
        genes = [i for i in 'LURD']
        gene = random.choice(genes)
        return str(gene)

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
            self.game = logic.add_new(self.game)
            self.fitness = self.calculate_fitness()

    def replace(self, exclude):
        genes = 'LURD'.replace(exclude, '')
        new_allele = random.choice(genes)
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
        while game_state == 'continue':
            tmp = [x[:] for x in self.game]
            count += 1
            if is_repeat:
                self.chromosome += self.replace(self.chromosome[-1])
            else:
                self.chromosome += self.mutate()
            self.perform_action(self.chromosome[-1])
            is_repeat = self.compare_game(tmp)
            game_state = logic.game_state(self.game)
        return game_state

    def mate(self, other):
        child = ''
        for p1, p2 in zip(self.chromosome, other.chromosome):
            prob = random.random()
            if prob < .35:
                child += p1
            elif prob < .7:
                child += p2
            else:
                child += self.mutate()
        return Player(child)

    def debug(self):
        print('Fitness: ' + str(self.fitness))
        print('Game: ')
        print(self.game)
        print('Chromosome: ' + self.chromosome)


    def calculate_fitness(self):
        score = logic.score(self.game)
        return score
