'''
Contributor(s): Thomas Hopkins

Contains the global constants used by the program to allow for easy
manipulation of key aspects of the game framework.
'''

GEOMETRY = '800x1000' # window dimensions
# tile colors
COLORS = {2: "#eee4da", 4: "#ede0c8", 8: "#f2b179",
          16: "#f59563", 32: "#f67c5f", 64: "#f65e3b",
          128: "#edcf72", 256: "#edcc61", 512: "#edc850",
          1024: "#edc53f", 2048: "#edc22e"}

# weights applied to positions on the game board
POSITION_TABLE = [[ 0, 0, 1, 3],
				  [ 0, 1, 3, 5],
				  [ 1, 3, 5, 15],
				  [ 3, 5, 15, 30]]
