'''
Contributor(s): Thomas Hopkins

Contains the global constants used by the program to allow for easy
manipulation of key aspects of the genetic algorithm.
'''
POPULATION_SIZE = 50
MUTATION_RATE = .3
EXTEND_SIZE = 25 # extend moveset of player by this amount
GENE_POOL = 'LURD' # (left, up, right, down) moveset
GEN_OFFSET = 10 # extend moveset of player after this many generations
ELITE = 10 # percentage of population size that survive to next generation