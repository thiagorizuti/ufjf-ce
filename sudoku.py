import random
import copy
from sys import argv
from datetime import datetime
import math
import time

#CLASS REPRESENTING A SUDOKU PUZZLE
class Sudoku(object):
    board = []
    fitness = -1

    def __init__(self, dimension):
        """Create a new sudoku given the dimension"""
        self.dimension = dimension

    def display(self):
        """Print the sudoku board"""
        for row in self.board:
            if self.dimension > 3:
                print " ".join("%02d" % x for x in row)
            else:
                print " ".join(str(x) for x in row)
        print "\n"

    def pre_process(self):
        """Pre process the sudoku puzzle solving the positions with one possible value"""
        count = 0
        for position_index in range(self.dimension**4):
            row_index = self.get_row_index(position_index)
            column_index = self.get_column_index(position_index)
            if self.board[row_index][column_index] == 0:
                values = [1 for x in range(1,self.dimension**2+1)]
                for value in self.get_row(position_index):
                    if value != 0:
                        values[value-1] = 0
                for value in self.get_column(position_index):
                    if value != 0:
                        values[value-1] = 0
                for value in self.get_block(position_index):
                    if value != 0:
                        values[value-1] = 0
                if sum(values) == 1:
                    self.board[row_index][column_index] = values.index(1) + 1
                    count +=1
        return count

    def get_row_index(self,position_index):
        return position_index/self.dimension**2

    def get_column_index(self,position_index):
        return position_index % self.dimension**2

    def get_row(self, position_index):
        """Returns a list containing the values of the row of the given position index"""
        row_index = position_index/self.dimension**2
        return self.board[row_index]

    def get_column(self, position_index):
        """Returns a list containing the values of the row of the given position index"""
        column_index = position_index % self.dimension**2
        column = []
        for i in range(0,self.dimension**2):
            column.append(self.board[i][column_index])
        return column

    def get_block(self, position_index):
        """Returns the coordinates of a block given the row and column of the element"""
        row_index = position_index/self.dimension**2
        column_index = position_index % self.dimension**2
        block_row_index = row_index / self.dimension
        block_column_index = column_index / self.dimension
        block = []
        for i in range(self.dimension*block_row_index,self.dimension*(block_row_index+1)):
            for j in range(self.dimension*block_column_index,self.dimension*(block_column_index+1)):
                block.append(self.board[i][j])
        return block

    def blocks_fitness(self):
        fit = 0
        v = [0 for x in range(self.dimension**2)]
        for m in range(self.dimension):
            for n in range(self.dimension):
                for i in range(m*self.dimension, m*self.dimension	 + self.dimension):
                    for j in range(n*self.dimension, n*self.dimension + self.dimension):
                        v[self.board[i][j]-1] += 1
                for x in v:
                    fit += abs(x-1)
                v = [0 for x in range(self.dimension**2)]
        return fit

    def columns_fitness(self):
        fit = 0
        for i in range(self.dimension**2):
            v = [0 for x in range(self.dimension**2)]
            for row in self.board:
                v[row[i]-1] += 1
            for x in v:
                fit += abs(x-1)
        return fit

    def calculate_fitness(self):
        """Calculate the fitness of the solution"""
        self.fitness = self.columns_fitness() + self.blocks_fitness();


    def rows_fitness(self):
        fit = 0
        for row in self.board:
            v = [0 for x in range(self.dimension**2)]
            for i in range(len(row)):
                v[row[i]-1] += 1
            for x in v:
                fit += abs(x-1)
        return fit


#CLASS REPRESENTING A POSSIBLE SOLUTION FOR A SUDOKU PUZZLE
class Solution(object):
    board = []
    fitness = -1
    chance = -1

    def __init__(self, sudoku):
        """Create a random solution for a given sudoku, guaranteeing the uniqueness of values in each row"""
        self.sudoku = sudoku
        self.board = copy.deepcopy(self.sudoku.board)
        for row in self.board:
            rand = [x for x in range(1,self.sudoku.dimension**2+1)]
            random.shuffle(rand)
            for i in range(len(row)):
                if row[i] == 0:
                    p = rand.pop(0)
                    while p in row:
                        p = rand.pop(0)
                    row[i] = p

    def display(self):
        """Print the solution board"""
        print self.fitness
        for row in self.board:
            if self.sudoku.dimension > 3:
                print " ".join("%02d" % x for x in row)
            else:
                print " ".join(str(x) for x in row)

        print "\n"

    def calculate_fitness(self):
        """Calculate the fitness of the solution"""
        if self.fitness == -1:
            self.fitness = self.columns_fitness() + self.blocks_fitness();


    def rows_fitness(self):
        fit = 0
        for row in self.board:
            v = [0 for x in range(self.sudoku.dimension**2)]
            for i in range(len(row)):
                v[row[i]-1] += 1
            for x in v:
                fit += abs(x-1)
        return fit

    def blocks_fitness(self):
        fit = 0
        v = [0 for x in range(self.sudoku.dimension**2)]
        for m in range(self.sudoku.dimension):
            for n in range(self.sudoku.dimension):
                for i in range(m*self.sudoku.dimension, m*self.sudoku.dimension	 + self.sudoku.dimension):
                    for j in range(n*self.sudoku.dimension, n*self.sudoku.dimension + self.sudoku.dimension):
                        v[self.board[i][j]-1] += 1
                for x in v:
                    fit += abs(x-1)
                v = [0 for x in range(self.sudoku.dimension**2)]
        return fit

    def columns_fitness(self):
        fit = 0
        for i in range(self.sudoku.dimension**2):
            v = [0 for x in range(self.sudoku.dimension**2)]
            for row in self.board:
                v[row[i]-1] += 1
            for x in v:
                fit += abs(x-1)
        return fit



#CLASS REPRESENTING A GENETIC ALGORITHMS, ITS PARAMETERS AND OPERATORS
class GA(object):
    population = []
    def __init__(self, sudoku, mt_rate, cx_rate, pop_size):
        self.sudoku = sudoku
        self.mt_rate = mt_rate
        self.cx_rate = cx_rate
        self.pop_size = pop_size

    def start_population(self):
        for i in range(self.pop_size):
            x = Solution(self.sudoku)
            if x not in self.population:
                self.population.append(x)

    def display_population(self):
        for ind in self.population:
            ind.display()
        print "\n"

    def mutation_swap(self,ind):
        if probabilty(self.mt_rate):
            r0 = random.randint(0,self.sudoku.dimension**2-1)
            r1 = random.randint(0,self.sudoku.dimension**2-1)
            while self.sudoku.board[r0][r1] != 0:
                r1 = random.randint(0,self.sudoku.dimension**2-1)
            r2 = random.randint(0,self.sudoku.dimension**2-1)
            while self.sudoku.board[r0][r2] != 0 and r2 != r1:
                r2 = random.randint(0,self.sudoku.dimension**2-1)
            aux = ind.board[r0][r1]
            ind.board[r0][r1] = ind.board[r0][r2]
            ind.board[r0][r2] = aux

    def mutation_5swap(self,ind):
        if probabilty(self.mt_rate):
            for i in range(5):
                r0 = random.randint(0,self.sudoku.dimension**2-1)
                r1 = random.randint(0,self.sudoku.dimension**2-1)
                while self.sudoku.board[r0][r1] != 0:
                    r1 = random.randint(0,self.sudoku.dimension**2-1)
                r2 = random.randint(0,self.sudoku.dimension**2-1)
                while self.sudoku.board[r0][r2] != 0 and r2 != r1:
                    r2 = random.randint(0,self.sudoku.dimension**2-1)
                aux = ind.board[r0][r1]
                ind.board[r0][r1] = ind.board[r0][r2]
                ind.board[r0][r2] = aux

    def mutation(self,ind):
        r = random.randint(0,4)
        for i in range(r):
            if probabilty(self.mt_rate):
                r0 = random.randint(0,self.sudoku.dimension**2-1)
                r1 = random.randint(0,self.sudoku.dimension**2-1)
                if self.sudoku.board[r1] == 0:
                    r2 = random.randint(0,self.sudoku.dimension**2-1)
                    if self.sudoku.board[r2] == 0:
                        aux = ind.board[r0][r1]
                        ind.board[r0][r1] = ind.board[r0][r2]
                        ind.board[r0][r2] = aux


    def shuffle(self,ind):
        for i in range(self.sudoku.dimension**2):
            rand = [x for x in range(self.sudoku.dimension**2+1)]
            random.shuffle(rand)
            for j in range(self.sudoku.dimension**2):
                if self.sudoku.board[i][j] == 0:
                    ind.board[i][j] = rand.pop(0)
        ind.fitness = -1

    def population_shuffle(self):
        for i in range(len(self.population)/3,len(self.population)):
            self.shuffle(self.population[i])

    def crossover(self,ind1, ind2):
        new_ind1 = copy.deepcopy(ind1)
        new_ind1.fitness = -1
        new_ind2 = copy.deepcopy(ind2)
        new_ind2.fitness = -1
        for i, row in enumerate(new_ind1.board):
            if probabilty(self.cx_rate):
                aux = copy.deepcopy(new_ind1.board[i])
                new_ind1.board[i] = copy.deepcopy(new_ind2.board[i])
                new_ind2.board[i] = copy.deepcopy(aux)
        return (new_ind1, new_ind2)

    def selection(self):
        tot = sum([ind.chance for ind in self.population])
        r = random.uniform(0,tot)
        for ind in self.population:
            r -= ind.chance
            if r <= 0:
                ind.chance = 0
                return ind

    def selection_rand(self):
        r = random.randint(0,len(self.population)-1)
        return self.population[r]

    def calculate_population_fitness(self):
        for ind in self.population:
            ind.calculate_fitness()

    def aging(self,ind):
        ind.fitness = ind.fitness + 1

    def equals(self,ind1,ind2):
        for i in len(ind1.board):
            if ind[i] != ind2[i]:
                return False
        return True

    def in_population(self,ind0):
        for ind in self.population:
            if equals(ind, ind0):
                return True
        return False

    def evolve(self,verbose):
        self.start_population()
        self.calculate_population_fitness()
        self.population.sort(key = lambda ind: ind.fitness)
        data=[]
        gen = 1
        best_fit = 99999
        best_count = 1
        local_minima = False
        while self.population[0].fitness != 0 and gen < 1000:
            new_population = []
            self.calculate_population_fitness()
            self.population.sort(key = lambda ind: ind.fitness)
            if self.population[0].fitness < best_fit:
                best_fit = self.population[0].fitness
                best_count = gen
                local_minima = False
            data.append(best_fit)
            if(best_fit == 0):
                break
            if gen - best_count > 50:
                #print "shuffle"
                self.population_shuffle()
                self.calculate_population_fitness()
                self.population.sort(key = lambda ind: ind.fitness)
                local_minima = True
            if verbose:
                print "Generation: ", gen, " Fittest: ", best_fit
            while len(new_population) < self.pop_size:
                for ind in self.population:
                    ind.chance = float(1)/ind.fitness
                if local_minima == True:
                    ind1 = self.selection_rand()
                    ind2 = self.selection_rand()
                else:
                    ind1 = self.selection()
                    ind2 = self.selection()
                new_ind = self.crossover(ind1, ind2)
                self.mutation_5swap(new_ind[0])
                self.mutation_5swap(new_ind[1])
                if new_ind[0] not in self.population:
                    new_ind[0].calculate_fitness
                    new_population.append(new_ind[0])
                if new_ind[1] not in self.population:
                    new_ind[1].calculate_fitness
                    new_population.append(new_ind[1])
            new_population.sort(key = lambda ind: ind.fitness)
            new_population = new_population[0:int(0.9*self.pop_size)]
            self.population = self.population[0:int(0.1*self.pop_size)]
            self.population = self.population + new_population
            gen +=1
        print gen
        print data


def probabilty(prob):
    r = random.random()
    return  r <= prob

def read_sudoku_file(file_name,dimension):
    sudoku = Sudoku(dimension)
    with open(file_name,"r") as file:
        content = file.readlines()
        for line in content:
            row = [int(n) for n in line.split()]
            sudoku.board.append(row)
	return sudoku

def str_to_bool(s):
    if s == 'True':
         return True
    elif s == 'False':
         return False

def main():
    if len(argv) < 3:
        print "First argument: file name.argument"
        print "Second argument: sudoku dimension"
        print "Third argument: random seed"
        print "Fourth argument: pre process - true or false"
        print "Fifth argument: verbose - true or false"
        return 1
    dim = int(argv[1])
    file_name = argv[2]
    seed = argv[3]
    preprocess = str_to_bool(argv[4])
    verbose = str_to_bool(argv[5])
    random.seed(datetime.now())
    print file_name
    sudoku = read_sudoku_file(file_name,dim)
    if preprocess:
        while(sudoku.pre_process()> 0):
            continue
    ga = GA(sudoku,0.4,0.3, 500)
    start = time.time()
    ga.evolve(verbose)
    end = time.time()
    print ga.population[0].fitness
    print(end - start)
    return 0

if __name__ == "__main__":
    main()
