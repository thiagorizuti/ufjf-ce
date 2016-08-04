import random
import copy
from sys import argv
from datetime import datetime
import math
import time


#CLASS REPRESENTING A SUDOKU PUZZLE
class Sudoku(object):

    def __init__(self):
        self.board = []
        self.dim = -1
        self.fit = -1
        self.chance = -1

    def fill_random(self):
        """Create a random solution guaranteeing the uniqueness of values in each row"""
        for row in self.board:
            rand = [x for x in range(1,self.dim+1)]
            random.shuffle(rand)
            for i in range(len(row)):
                if row[i] == 0:
                    p = rand.pop(0)
                    while p in row:
                        p = rand.pop(0)
                    row[i] = p

    def display(self):
        """Print the sudoku board"""
        print self.fit
        for row in self.board:
            if self.dim > 9:
                print " ".join("%02d" % x for x in row)
            if self.dim > 81:
                print " ".join("%03d" % x for x in row)
            else:
                print " ".join(str(x) for x in row)

        print "\n"

    def calculate_fitness(self):
        """Calculate the fitness of the solution"""
        if self.fit == -1:
            self.fit = self.columns_fitness() + self.blocks_fitness()

    def columns_fitness(self):
        """Calculate the parcial fitness of each column"""
        fit = 0
        for i in range(self.dim):
            v = [0 for x in range(self.dim)]
            for row in self.board:
                v[row[i]-1] += 1
            for x in v:
                if(x != 0):
                    fit += x-1
        return fit

    def blocks_fitness(self):
        """Calculate the parcial fitness of each block"""
        fit = 0
        v = [0 for x in range(self.dim)]
        d = int(math.sqrt(self.dim))
        for m in range(d):
            for n in range(d):
                for i in range(m*d, m*d	+ d):
                    for j in range(n*d, n*d + d):
                        v[self.board[i][j]-1] += 1
                for x in v:
                    if(x != 0):
                        fit += x-1
                v = [0 for x in range(self.dim)]
        return fit

#CLASS REPRESENTING A GENETIC ALGORITHMS, ITS PARAMETERS AND OPERATORS
class GA(object):

    def __init__(self, sudoku, mt_rate, cx_rate, pop_size):
        self.sudoku = sudoku
        self.mt_rate = mt_rate
        self.cx_rate = cx_rate
        self.pop_size = pop_size
        self.pop = []

    def start_population(self):
        """Start the population with random individuals"""
        for i in range(self.pop_size):
            x = copy.deepcopy(self.sudoku)
            x.fill_random()
            if x not in self.pop:
                self.pop.append(x)

    def mutation_swap(self,ind):
        """Mutation operator. Does 5 swaps in a row given a propability"""
        if probabilty(self.mt_rate):
            for i in range(5):
                r0 = random.randint(0,self.sudoku.dim-1)
                r1 = random.randint(0,self.sudoku.dim-1)
                while self.sudoku.board[r0][r1] != 0:
                    r1 = random.randint(0,self.sudoku.dim-1)
                r2 = random.randint(0,self.sudoku.dim-1)
                while self.sudoku.board[r0][r2] != 0 and r2 != r1:
                    r2 = random.randint(0,self.sudoku.dim-1)
                aux = ind.board[r0][r1]
                ind.board[r0][r1] = ind.board[r0][r2]
                ind.board[r0][r2] = aux

    def crossover(self,ind1, ind2):
        """crossover operator. Trade lines between individuals"""
        new_ind1 = copy.deepcopy(ind1)
        new_ind1.fit = -1
        new_ind2 = copy.deepcopy(ind2)
        new_ind2.fit = -1
        for i, row in enumerate(new_ind1.board):
            if probabilty(self.cx_rate):
                aux = copy.deepcopy(new_ind1.board[i])
                new_ind1.board[i] = copy.deepcopy(new_ind2.board[i])
                new_ind2.board[i] = copy.deepcopy(aux)
        return (new_ind1, new_ind2)

    def roulette_selection(self):
        """Fitness proportionate random selection.]"""
        tot = sum([ind.chance for ind in self.pop])
        r = random.uniform(0,tot)
        for ind in self.pop:
            r -= ind.chance
            if r <= 0:
                ind.chance = 0
                return ind

    def tournament_selection(self):
        """Tournament selection with size 2"""
        r1 = random.randint(0,len(self.pop)-1)
        r2 = random.randint(0,len(self.pop)-1)
        if self.pop[r1].fit < self.pop[r2].fit:
            return self.pop[r1]
        return self.pop[r1]

    def calculate_population_fitness(self):
        """Calculate the fitness of each individual in population"""
        for ind in self.pop:
            ind.calculate_fitness()

    def start(self,file_name,seed,verbose):
        """Start the evolution process"""
        self.start_population()
        self.calculate_population_fitness()
        data=[]
        gen = 1
        best_fit = 99999
        best_count = 1
        while best_fit != 0 and gen < 500:
            new_population = []
            self.pop.sort(key = lambda ind: ind.fit)
            if self.pop[0].fit < best_fit:
                best_fit = self.pop[0].fit
                best_count = gen
            data.append(best_fit)
            if(best_fit == 0):
                break
            if(gen - best_count) > 100:
                break
            if verbose:
                print "Generation: ", gen, " Fittest: ", best_fit, best_count, (gen - best_count)
            while len(new_population) < self.pop_size:
                for ind in self.pop:
                    ind.chance = float(1)/ind.fit
                ind1 = self.roulette_selection()
                ind2 = self.roulette_selection()
                new_ind = self.crossover(ind1, ind2)
                self.mutation_swap(new_ind[0])
                self.mutation_swap(new_ind[1])
                new_ind[0].calculate_fitness()
                new_population.append(new_ind[0])
                new_ind[1].calculate_fitness()
                new_population.append(new_ind[1])
            new_population.sort(key = lambda ind: ind.fit)
            new_population = new_population[0:int(0.9*self.pop_size)]
            self.pop = self.pop[0:int(0.1*self.pop_size)]
            self.pop = self.pop + new_population
            gen +=1
        print file_name+str(seed)+" =",data


def probabilty(prob):
    "Given a probabilty determines if the event is going to happen or not"
    r = random.random()
    return  r <= prob

def read_sudoku_file(file_name):
    "Read a sudoku puzzle from file"
    sudoku = Sudoku()
    with open(file_name,"r") as file:
        content = file.readlines()
        for line in content:
            row = [int(n) for n in line.split()]
            sudoku.board.append(row)
        dim = 0
        for elem in row:
            dim += 1
        sudoku.dim = dim
	return sudoku

def str_to_bool(s):
    "Parse a string to boolean"
    if s == 'True':
         return True
    elif s == 'False':
         return False

def main():
    if len(argv) < 4:
        print "1st argument: file name"
        print "2nd argument: random seed"
        print "3rd argument: verbose (true or false)"
        return 1
    file_name = argv[1]
    seed = int(argv[2])
    verbose = str_to_bool(argv[3])
    random.seed(seed)
    sudoku = read_sudoku_file(file_name)
    ga = GA(sudoku,0.3,0.5, 500)
    start = time.time()
    ga.start(file_name,seed,verbose)
    end = time.time()
    print file_name + "-time" + str(seed) + " =", (end - start)
    return 0

if __name__ == "__main__":
    main()
