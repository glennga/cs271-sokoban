import random
import copy
import numpy as np 

class Game:
	def __init__(self, sizeH, sizeV, wallSquares, Boxes, storLocs, startLoc):
		# sizeH = int, sizeZ = int, wallSquares = list of tuples
		# Boxes = list of tuples, storLocs = list of tuples, startLoc = tuple
		self.sizeH = sizeH
		self.sizeV = sizeV 
		self.wallSquares = wallSquares
		self.Boxes = Boxes
		self.storLocs = storLocs
		self.currLoc = startLoc

def createGame(fname):
	f = open(fname) #for whatever relevant file

	specs = []

	line1 = f.readline()
	specs.append(int(line1[0])) # horizontal size
	specs.append(int(line1[2])) # vertical size

	line2 = f.readline()
	real_start = line2.find(' ') + 1 #the first value in this line is the number of wall squares
	real_line2 = line2[real_start:-1] #which doesnt actually matter, also taking out \n
	num_squares = ((len(real_line2) // 2) + 1) // 2

	wall_list = [] #list of wallSquares
	for i in range(num_squares):
		x = int(real_line2[4 * i])
		y = int(real_line2[(4 * i) + 2])
		wall_list.append((x,y))

	specs.append(wall_list)

	line3 = f.readline()
	real_start = line3.find(' ') + 1 #the first value in this line is the number of boxes
	real_line3 = line3[real_start:-1] #which doesnt actually matter, also taking out \n
	num_boxes = ((len(real_line3) // 2) + 1) // 2

	box_list = [] #list of boxes
	for i in range(num_boxes):
		x = int(real_line3[4 * i])
		y = int(real_line3[(4 * i) + 2])
		box_list.append((x,y))

	specs.append(box_list)


	line4 = f.readline()
	real_start = line4.find(' ') + 1 #the first value in this line is the number of boxes
	real_line4 = line4[real_start:-1] #which doesnt actually matter, also taking out \n
	num_locs = ((len(real_line4) // 2) + 1) // 2

	loc_list = [] #list of storage locs
	for i in range(num_locs):
		x = int(real_line4[4 * i])
		y = int(real_line4[(4 * i) + 2])
		loc_list.append((x,y))

	specs.append(loc_list)


	line5 = f.readline()
	start_loc = (int(line5[0]), int(line5[2]))

	specs.append(start_loc)

	our_game = Game(specs[0], specs[1], specs[2], specs[3], specs[4], specs[5])

	return our_game


def legal_moves(currState):
	moves = []

	down_loc = (currState.currLoc[0] + 1, currState.currLoc[1])
	if down_loc in currState.Boxes:
		two_away = (down_loc[0] + 1, down_loc[1])
		if two_away not in currState.Boxes and two_away not in currState.wallSquares:
			moves.append(0)
	if down_loc not in currState.Boxes and down_loc not in currState.wallSquares:
		moves.append(0)

	up_loc = (currState.currLoc[0] - 1, currState.currLoc[1])
	if up_loc in currState.Boxes:
		two_away = (up_loc[0] - 1, up_loc[1])
		if two_away not in currState.Boxes and two_away not in currState.wallSquares:
			moves.append(1)
	if up_loc not in currState.Boxes and up_loc not in currState.wallSquares:
		moves.append(1)

	right_loc = (currState.currLoc[0], currState.currLoc[1] + 1)
	if right_loc in currState.Boxes:
		two_away = (right_loc[0], right_loc[1] + 1)
		if two_away not in currState.Boxes and two_away not in currState.wallSquares:
			moves.append(2)
	if right_loc not in currState.Boxes and right_loc not in currState.wallSquares:
		moves.append(2)

	left_loc = (currState.currLoc[0], currState.currLoc[1] - 1)
	if left_loc in currState.Boxes:
		two_away = (left_loc[0], left_loc[1] - 1)
		if two_away not in currState.Boxes and two_away not in currState.wallSquares:
			moves.append(3)
	if left_loc not in currState.Boxes and left_loc not in currState.wallSquares:
		moves.append(3)

	return moves



def solved(currState):
	return set(currState.Boxes) == set(currState.storLocs)




def makeMove(state, move):

	_H = state.sizeH
	_V = state.sizeV
	_wallSquares = state.wallSquares
	_Boxes = state.Boxes
	_storLocs = state.storLocs
	_currLoc = state.currLoc

	newState = Game(_H, _V, _wallSquares, _Boxes, _storLocs, _currLoc)

	if move == 0:
		down_loc = (newState.currLoc[0] + 1, newState.currLoc[1])
		two_away = (down_loc[0] + 1, down_loc[1])
		newState.currLoc = down_loc
		if down_loc in newState.Boxes:
			newState.Boxes.remove(down_loc)
			newState.Boxes.append(two_away)
			
	if move == 1:
		up_loc = (newState.currLoc[0] - 1, newState.currLoc[1])
		two_away = (up_loc[0] - 1, up_loc[1])
		newState.currLoc = up_loc
		if up_loc in newState.Boxes:
			newState.Boxes.remove(up_loc)
			newState.Boxes.append(two_away)
			
	if move == 2:
		right_loc = (newState.currLoc[0], newState.currLoc[1] + 1)
		two_away = (right_loc[0], right_loc[1] +1)
		newState.currLoc = right_loc
		if right_loc in newState.Boxes:
			newState.Boxes.remove(right_loc)
			newState.Boxes.append(two_away)
			
	if move == 3:
		left_loc = (newState.currLoc[0], newState.currLoc[1] - 1)
		two_away = (left_loc[0], left_loc[1] - 1)
		newState.currLoc = left_loc
		if left_loc in newState.Boxes:
			newState.Boxes.remove(left_loc)
			newState.Boxes.append(two_away)

	return newState


def possibleStates(currState):
	A = legal_moves(currState)
	NextStates = []
	for i in range(len(A)):
		Action = A[i]
		NextState = makeMove(currState, Action)
		NextStates.append(NextState)

	return NextStates

def pickpossState(currState):
	A = legal_moves(currState)
	i = np.random.randint(0, len(A))
	Action = A[i]
	NextState = makeMove(currState, Action)
	return NextState

def GetStateRepresentation(currState):
	return currState.currLoc


def getResult(currState):
	box_set = set(currState.Boxes)
	stor_set = set(currState.storLocs)

	in_place = len(box_set & stor_set)

	bad_boxes = 0
	for box in currState.Boxes:
		if inBadCorner(box, currState):
			bad_boxes += 1

	return 10 + in_place - bad_boxes

def inBadCorner(loc, currState):
	x = loc[0]
	y = loc[1]
	if (x,y) in currState.storLocs: 
		return False
	if (x-1, y) in currState.wallSquares and (x, y+1) in currState.wallSquares:
		return True
	if (x+1, y) in currState.wallSquares and (x, y-1) in currState.wallSquares:
		return True
	if (x, y+1) in currState.wallSquares and (x+1, y) in currState.wallSquares:
		return True
	if (x, y-1) in currState.wallSquares and (x-1, y) in currState.wallSquares:
		return True
	return False


