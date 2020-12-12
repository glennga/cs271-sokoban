import __init__
import mctsnode as nd
import numpy as np
import game_model_old as game
import logging
import math
from hungarian_algorithm import algorithm


logger = logging.getLogger(__name__)

class MCTS:

	def __init__(self, Node):
		self.root = Node

	def pickChild(self, Node):

		selected = Node

		if (len(Node.children) == 0):
			return selected

		for Child in Node.children:
			if Child.visits == 0.0:
				# print("why no visits")
				return Child

		maxUTC = 0.0
		for child in Node.children:
			thisUTC = child.sputc 
			if(thisUTC > maxUTC):
				maxUTC = thisUTC
				selected = child
		return selected

	def selection(self):
		selected = self.root
		
		hasChild = False
		if(len(selected.children) > 0):
			hasChild = True

		while(hasChild):
			selected = self.pickChild(selected)
			if(len(selected.children) == 0):
				hasChild = False

		return selected

	def manhattanDistance(self, coordinate_1, coordinate_2):
		return abs(coordinate_1[0] - coordinate_2[0]) + abs(coordinate_1[1] - coordinate_2[1])

	def euclidian_distance (self, coordinate_1, coordinate_2):
		return math.sqrt((coordinate_1[0] - coordinate_2[0])**2 + (coordinate_1[1] - coordinate_2[1])**2)

	def euclidian_perfect_matching(self, boxes, targets):
		box_dict = {}
		target_dict = {}
		for i in range(1, len(boxes) + 1):
			box_dict[i] = boxes[i-1]
			target_dict[i+1000] = targets[i-1]
		
		
		bp_graph = {}
		for box in box_dict.keys():
			for target in target_dict.keys():
				weight = self.euclidian_distance(box_dict[box], target_dict[target])
				if box in bp_graph:
					bp_graph[box][target] = weight
					
				else:
					bp_graph[box] = {}
					bp_graph[box][target] = weight

		return algorithm.find_matching(bp_graph, matching_type = 'min', return_type = 'total')
	
		
	
	def manhattan_perfect_matching(self):
		pass
	
	def findChildren(self, Node):
		nextStates = game.possibleStates(Node.state)
		children = []
		for state in nextStates:
			ChildNode = nd.Node(state)
			boxes = ChildNode.state.Boxes
			targets = ChildNode.state.storLocs
			#c_heuristic = euclidean_perfect_matching(boxes, targets)
			ChildNode.heuristic = self.euclidian_perfect_matching(boxes, targets)
			children.append(ChildNode)
			
		heur_weights = []
		for child in children:
			heur_weights.append(child.heuristic)
			
		total_weight = sum(heur_weights)*1.0
		if total_weight == 0:
			prob_list = [0 for _ in heur_weights]
		else:
			prob_list = [weight/total_weight for weight in heur_weights]
			prob_list = prob_list[::-1]

		for i in range(len(children)):
			children[i].weighted_heuristic = prob_list[i]
		
		return children

	def pickChildNode(self, Node):
		# if np.random.random() > 0.8:
		num_children = len(Node.children)
		i = np.random.randint(0, num_children)
		return Node.children[i]
		# else:
		# 	return max(Node.children, key=lambda a: a.weighted_heuristic)


	def expansion(self, Leaf):
		if(game.isTerminal(Leaf.state)):
			logger.info('Game has reached a terminal state.')
			logger.debug(f'Current game state: \n{Leaf.state}')
			return False
		elif(Leaf.visits == 0):
			# print ("yea wtf no visits")
			return Leaf
		else:
			if(len(Leaf.children) == 0):
				children = self.findChildren(Leaf)
				for newChild in children:
					if newChild.state == Leaf.state:
						continue
					Leaf.AppendChild(newChild)
			child = self.pickChildNode(Leaf)
		logger.debug(f'Expanded: {game.GetStateRepresentation(child.state)}')
		return child


	def simulation(self, Node, bound):
		currState = Node.state

		count = 0

		while(not(game.isTerminal(currState)) and count < bound):
			currState = game.pickpossState(currState)
			count += 1
			logger.debug(f'Current state: {game.GetStateRepresentation(currState)}')

		result = game.getResult(currState)
		return result


	def isDescendant(self, Node):
		if(Node.parent == None):
			return False
		return True


	def backpropagation(self, Node, Result):
		currNode = Node
		currNode.wins += Result
		currNode.ressq += Result ** 2
		currNode.visits += 1
		self.calcUTC(currNode)

		while(self.isDescendant(currNode)):
			currNode = currNode.parent
			currNode.wins += Result
			currNode.ressq += Result ** 2
			currNode.visits += 1
			self.calcUTC(currNode)

	
	def calcUTC(self, Node):
		c = 0.5
		w = Node.wins
		n = Node.visits
		sumsq = Node.ressq 
		if(Node.parent == None):
			t = Node.visits
		else:
			t = Node.parent.visits

		# UTC = 0.5*(w/n + c * np.sqrt(np.log(t) / n)) + 0.5*Node.weighted_hueristic
		UTC = (w/n + c * np.sqrt(np.log(t) / n))

		#D = 1000

		#Modification = np.sqrt((sumsq - n * (w/n)**2 + D)/n)

		Node.sputc = UTC # + Modification
		return Node.sputc

	def run(self, iters = 10000):
		for i in range(iters):
			logger.debug(f'==== Starting iteration {i}. ==== ')
			X = self.selection()
			Y = self.expansion(X)
			if(Y):
				Result = self.simulation(Y, 100)
				logger.debug(f'Result of simulation: {Result}')
				self.backpropagation(Y, Result)
			else:
				Result = game.getResult(X.state)
				logger.debug(f'Result of simulation: {Result}')
				self.backpropagation(X, Result)
		

		logger.info(f'Search complete. Iterations = {i}')

	def display_moves(self):
		""" Traverse our root to a terminal state, choosing the most "winning" nodes along the way. """
		logger.info('Now printing the solution to console. ')
		output_str = ''

		current_node = self.root
		i = 0  # Current step count.
		logger.debug(f'{i}. Starting state.')

		previous_move, current_move_count = None, 1
		while len(current_node.children) != 0:
			current_node = max(current_node.children, key=lambda x: x.wins)
			current_move = current_node.state.move_taken

			logger.debug(f'{i} Taking {str(current_move)}.')
			if previous_move != current_move:
				output_str = output_str +  f'{current_move_count} {str(current_node.state.move_taken)} '
				current_move_count = 1
			else:
				current_move_count = current_move_count + 1
			previous_move = current_move

		output_str = output_str + f'{current_move_count} {str(current_node.state.move_taken)} '
		logger.info(f'In project format: {output_str}.')
		print(output_str)
