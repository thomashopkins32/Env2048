from game.game import GameState
import expectimax.constants as const

class ExpectimaxAgent():


	def getAction(self, game_state):
		return self.maxValue(game_state, 0)


	def maxValue(self, game_state, depth):
		if game_state.lost:
			return game_state.get_score()
		actions = const.MOVESET
		best_score = float('inf')
		best_action = None
		for action in actions:
			score = self.expectedValue(game_state.generate_successor(action), depth)
			if score > best_score:
				score = best_score
				best_action = action
		if depth == const.MAX_DEPTH:
			return best_action
		else:
			return best_score


	def expectedValue(self, game_state, depth):
		if game_state.lost or depth == const.MAX_DEPTH:
			return game_state.get_score()
		possible_states = game_state.possible_random_states() #TODO: return list of (state, prob of occurrence)
		score = 0
		for state, prob in possible_states:
			score += (self.maxValue(state, depth+1)*prob)
		return score
