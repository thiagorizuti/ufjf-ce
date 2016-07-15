import random
import copy

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
    fitness = -1

    def __init__(self, sudoku):
        self.sudoku = sudoku
        self.board = copy.deepcopy(self.sudoku.board)
        for row in self.board:
            rand = [x for x in range(1,self.sudoku.dim**2+1)]
            random.shuffle(rand)
            for i in range(len(row)):
                if row[i] == 0:
                    row[i] = rand.pop(0)

    def display(self):
        print "\n"
        for row in self.board:
            print " ".join(str(x) for x in row)

    def get_fitness(self):
        if self.fitness != -1:
            return self.fitness
        else:
            return self.calculate_fitness()


    def calculate_fitness(self):
        return self.rows_fitness() + self.columns_fitness() + self.blocks_fitness();


    def rows_fitness(self):
        fit = 0
        for row in self.board:
            v = [0 for x in range(self.sudoku.dim**2)]
            for i in range(len(row)):
                v[row[i]-1] += 1
            for x in v:
                fit += abs(x-1)
        return fit


    def blocks_fitness(self):
        fit = 0
        v = [0 for x in range(self.sudoku.dim**2)]
        for m in range(self.sudoku.dim):
            for n in range(self.sudoku.dim):
                for i in range(m*self.sudoku.dim, m*self.sudoku.dim	 + self.sudoku.dim):
                    for j in range(n*self.sudoku.dim, n*self.sudoku.dim + self.sudoku.dim):
                        v[self.board[i][j]-1] += 1
                for x in v:
                    fit += abs(x-1)
                v = [0 for x in range(self.sudoku.dim**2)]
        return fit

    def columns_fitness(self):
        fit = 0
        for i in range(self.sudoku.dim**2):
            v = [0 for x in range(self.sudoku.dim**2)]
            for row in self.board:
                v[row[i]-1] += 1
            for x in v:
                fit += abs(x-1)
        return fit


class GA(object):
    pop = []
    def __init__(self, sudoku, mt_rate, cx_rate, pop_size):
        self.sudoku = sudoku
        self.mt_rate = mt_rate
        self.cx_rate = cx_rate
        self.pop_size = pop_size

    def start_pop(self):
        for i in range(self.pop_size):
            self.pop.append(Solution(self.sudoku))

    def display_pop(self):
        for ind in self.pop:
            ind.display()
        print "\n"

    def mutation(ind):
        pass

    def crossover(ind):
        pass


sdk = Sudoku(3)
ga = GA(sdk,0.5,0.6,20)
ga.start_pop()
ga.pop[1].display()
print ga.pop[1].get_fitness()

