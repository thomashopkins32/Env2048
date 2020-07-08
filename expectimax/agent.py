from game.game import GameState
import expectimax.constants as const

class ExpectimaxAgent():
	def __init__(self):
		pass

	def getAction(self, game_state):
		return self.maxValue(game_state, 0)


	def maxValue(self, game_state, depth):
		if game_state.lost:
			return game_state.get_score()
		actions = const.MOVESET
		best_score = float('-inf')
		best_action = None
		for action in actions:
			score = self.expectedValue(game_state.generate_successor(action), depth+1)
			if score > best_score:
				best_score = score
				best_action = action
		if depth == const.MAX_DEPTH:
			print(best_action)
			return best_action
		else:
			return best_score


	def expectedValue(self, game_state, depth):
		if game_state.lost or depth == const.MAX_DEPTH:
			return game_state.get_score()
		possible_states = game_state.possible_random_states()
		score = 0
		for state, prob in possible_states:
			score += int(float(self.maxValue(state, depth+1))*prob)
		return score
