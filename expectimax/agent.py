from game.game import GameState
import expectimax.constants as const

class ExpectimaxAgent():
	def __init__(self):
		self.game = GameState()
		self.initial_state = self.game.get_board()
		self.score = 0
		self.turn_counter = 0
		self.all_moves = ''

	def expectimax_alg(self, node, depth):
		if depth == const.MAX_DEPTH or node.lost:
			return self.calculate_score(node)
		make_move = self.turn_counter % 2 == 0
		if make_move:
			v = float('-inf')
			for move in const.MOVESET:
				new_game = self.game.perform_action(move, new_game_state=True)
				v = max(v, self.expectimax_alg(new_game, depth-1))
		else:
			# TODO: chance node
			# cant use perform action above since it takes both turns at once
			# add functionality to GameState for methods that return new instances
			# of GameState




