import random

# read from a sokoban file instance

f = open("sok_input1.txt") #for whatever relevant file

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

print(specs)

# this completes reading from the given input file


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

	def legal_moves(self):
		moves = []

		down_loc = (self.currLoc[0] + 1, self.currLoc[1])
		if down_loc in self.Boxes:
			two_away = (down_loc[0] + 1, down_loc[1])
			if two_away not in self.Boxes and two_away not in self.wallSquares:
				moves.append('d')
		if down_loc not in self.Boxes and down_loc not in self.wallSquares:
			moves.append('d')

		up_loc = (self.currLoc[0] - 1, self.currLoc[1])
		if up_loc in self.Boxes:
			two_away = (up_loc[0] - 1, up_loc[1])
			if two_away not in self.Boxes and two_away not in self.wallSquares:
				moves.append('u')
		if up_loc not in self.Boxes and up_loc not in self.wallSquares:
			moves.append('u')

		right_loc = (self.currLoc[0], self.currLoc[1] + 1)
		if right_loc in self.Boxes:
			two_away = (right_loc[0], right_loc[1] + 1)
			if two_away not in self.Boxes and two_away not in self.wallSquares:
				moves.append('r')
		if right_loc not in self.Boxes and right_loc not in self.wallSquares:
			moves.append('r')

		left_loc = (self.currLoc[0], self.currLoc[1] - 1)
		if left_loc in self.Boxes:
			two_away = (left_loc[0], left_loc[1] - 1)
			if two_away not in self.Boxes and two_away not in self.wallSquares:
				moves.append('l')
		if left_loc not in self.Boxes and left_loc not in self.wallSquares:
			moves.append('l')

		return moves

	def implement_move(self, move):
		# move is one of r,l,u,d
		
		if move == 'd':
			down_loc = (self.currLoc[0] + 1, self.currLoc[1])
			two_away = (down_loc[0] + 1, down_loc[1])
			self.currLoc = down_loc
			if down_loc in self.Boxes:
				self.Boxes.remove(down_loc)
				self.Boxes.append(two_away)
				
		if move == 'u':
			up_loc = (self.currLoc[0] - 1, self.currLoc[1])
			two_away = (up_loc[0] - 1, up_loc[1])
			self.currLoc = up_loc
			if up_loc in self.Boxes:
				self.Boxes.remove(up_loc)
				self.Boxes.append(two_away)
				
		if move == 'r':
			right_loc = (self.currLoc[0], self.currLoc[1] + 1)
			two_away = (right_loc[0], right_loc[1] +1)
			self.currLoc = right_loc
			if right_loc in self.Boxes:
				self.Boxes.remove(right_loc)
				self.Boxes.append(two_away)
				
		if move == 'l':
			left_loc = (self.currLoc[0], self.currLoc[1] - 1)
			two_away = (left_loc[0], left_loc[1] - 1)
			self.currLoc = left_loc
			if left_loc in self.Boxes:
				self.Boxes.remove(left_loc)
				self.Boxes.append(two_away)

	def solved(self):
		return set(self.Boxes) == set(self.storLocs)


our_game = Game(specs[0], specs[1], specs[2], specs[3], specs[4], specs[5])

print(our_game.solved())

poss_moves = our_game.legal_moves()

print(poss_moves)

our_game.implement_move(random.choice(poss_moves))

print(our_game.solved())
