import __init__
import mctsnode as nd
import numpy as np
import game_model as game
import logging

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
				print("why no visits")
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


	def findChildren(self, Node):
		nextStates = game.possibleStates(Node.state)
		children = []
		for state in nextStates:
			ChildNode = nd.Node(state)
			children.append(ChildNode)

		return children

	def pickChildNode(self, Node):
		num_children = len(Node.children)
		i = np.random.randint(0, num_children)
		return Node.children[i]


	def expansion(self, Leaf):
		if(game.isTerminal(Leaf.state)):
			logger.info('Game has reached a terminal state.')
			logger.debug(f'Current game state: \n{Leaf.state}')
			return False
		elif(Leaf.visits == 0):
			print ("yea wtf no visits")
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

		UTC = w/n + c * np.sqrt(np.log(t) / n)

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
				Result = self.simulation(Y, 20)
				logger.debug(f'Result of simulation: {Result}')
				self.backpropagation(Y, Result)
			else:
				Result = game.getResult(X.state)
				logger.debug(f'Result of simulation: {Result}')
				self.backpropagation(X, Result)
		

		logger.info(f'Search complete. Iterations = {i}')

