'''
Contributor(s): Thomas Hopkins

Contains the global constants used by the program to allow for easy
manipulation of key aspects of the genetic algorithm.
'''
POPULATION_SIZE = 1000
MUTATION_RATE = .3
EXTEND_SIZE = 25 # extend moveset of player by this amount
GENE_POOL = 'LURD' # (left, up, right, down) moveset
GEN_OFFSET = 10 # extend moveset of player after this many generations
ELITE = .1 # proportion of population size that survive to next generation
# weights applied to positions on the game board
POSITION_TABLE = [[ 0, 0, 1, 3],
				  [ 0, 1, 3, 5],
				  [ 1, 3, 5, 15],
				  [ 3, 5, 15, 30]]