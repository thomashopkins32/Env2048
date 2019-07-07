from numpy import random

R_GLOBAL = random.RandomState(21)
POPULATION_SIZE = 100
MUTATION_RATE = .3
EXTEND_SIZE = 25
GENE_POOL = 'LURD'
GEN_OFFSET = 10
ELITE = 5


GEOMETRY = '800x1000'
COLORS = {2: "#eee4da", 4: "#ede0c8", 8: "#f2b179",
                         16: "#f59563", 32: "#f67c5f", 64: "#f65e3b",
                         128: "#edcf72", 256: "#edcc61", 512: "#edc850",
                         1024: "#edc53f", 2048: "#edc22e"}
