from numpy import random

R_GLOBAL = random.RandomState(21) # random state for mutations/mating
POPULATION_SIZE = 50
MUTATION_RATE = .3
EXTEND_SIZE = 25 # extend moveset of player by this amount
GENE_POOL = 'LURD' # (left, up, right, down) moveset
GEN_OFFSET = 10 # extend moveset of player after this many generations
ELITE = 10 # percentage of population size that survive to next generation


GEOMETRY = '800x1000' # window dimensions
# tile colors
COLORS = {2: "#eee4da", 4: "#ede0c8", 8: "#f2b179",
                         16: "#f59563", 32: "#f67c5f", 64: "#f65e3b",
                         128: "#edcf72", 256: "#edcc61", 512: "#edc850",
                         1024: "#edc53f", 2048: "#edc22e"}
