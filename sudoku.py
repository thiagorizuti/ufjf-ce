from random import randint

class Sudoku(object):
	board = [[0,4,0,0,0,0,1,7,9],
		 [0,0,2,0,0,8,0,5,4],
		 [0,0,6,0,0,5,0,0,8],
		 [0,8,0,0,7,0,9,1,0],
		 [0,5,0,0,9,0,0,3,0],
		 [0,1,9,0,6,0,0,4,0],
		 [3,0,0,4,0,0,7,0,0],
		 [5,7,0,1,0,0,2,0,0],
		 [9,2,8,0,0,0,0,6,0]]
	def __init__(self, dim):
		self.dim = dim
	
	def display(self):
		print "\n"
		for row in self.board:
        		print " ".join(str(x) for x in row)


class Solution(object):
	board = []
	def __init__(self, sudoku):
		self.sudoku = sudoku
		self.board = self.sudoku.board[:]
		for row in self.board:
			#for x in row:
				if x == 0:
					x = 8
					#x = randint(1,self.sudoku.dim**2)
				 	#while r in row:
					#	r = randint(1,self.sudoku.dim**2)
					#x = -1

	def display(self):
		print "\n"
		for row in self.board:
        		print " ".join(str(x) for x in row)

class GA(object):
	pop = []
	def __init__(self, sudoku, mt_rate, cx_rate, pop_size):
		self.sudoku = sudoku		
		self.mt_rate = mt_rate
		self.cx_rate = cx_rate
		self.pop_size = pop_size
	
	def start_pop(self):
		for i in range(self.pop_size):
			ind = Solution(self.sudoku)
			self.pop.append(ind)
	
	def display_pop(self):
		for ind in self.pop:
			ind.display()
			print "\n"
		
		
sdk = Sudoku(3)
sdk.display()
#ga = GA(sdk,0.5,0.6,20)
ind = Solution(sdk)
ind.display()
#ga.start_pop()
#ga.display_pop()
