from numpy import random
import logic

class Player(object):
    def __init__(self, chromosome):
        self.genes = 'LURD'
        self.chromosome = chromosome
        self.game = logic.new_game()
        self.game = logic.add_new(self.game)
        self.game = logic.add_new(self.game)
        self.outcome = self.simulate()

    def mutate(self):
        gene = random.choice(self.genes)
        return gene

    def create_genome(self):
        max_genes = 10000
        return [self.mutate() for i in range(max_genes)]

    def simulate(self):
        game_state = ''
        tmp = [x[:] for x in self.game]
        count = 0
        for i in self.chromosome:
            count += 1
            if i == 'R':
                self.game = logic.right(self.game)
            elif i == 'L':
                self.game = logic.left(self.game)
            elif i == 'U':
                self.game = logic.up(self.game)
            elif i == 'D':
                self.game = logic.down(self.game)
            if tmp != self.game:
                self.game = logic.add_new(self.game)
                self.fitness = self.calculate_fitness()
                game_state = logic.game_state(self.game)
                if game_state != 'continue':
                    break
        self.chromosome = self.chromosome[:count]
        return game_state

    def mate(self, other):
        child = []
        for p1, p2 in zip(self.chromosome, other.chromosome):
            prob = random.random()
            if prob < .45:
                child.append(p1)
            elif prob < .9:
                child.append(p2)
            else:
                child.append(self.mutate())
        return Player(child)

    def calculate_fitness(self):
        score = logic.score(self.game)
        return score
