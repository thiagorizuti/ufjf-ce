import random
import copy

class Sudoku(object):
    board = [[0,0,2,0,0,0,5,0,0],
             [0,1,0,7,0,5,0,2,0],
             [4,0,0,0,9,0,0,0,7],
             [0,4,9,0,0,0,7,3,0],
             [8,0,1,0,3,0,4,0,9],
             [0,3,6,0,0,0,2,1,0],
             [2,0,0,0,8,0,0,0,4],
             [0,8,0,9,0,2,0,6,0],
             [0,0,7,0,0,0,8,0,0]]


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


    def calculate_fitness(self):
        self.fitness = self.columns_fitness() + self.blocks_fitness();


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

    def mutation_swap(self,ind):
        if probabilty(self.mt_rate):
            r0 = random.randint(0,self.sudoku.dim**2-1)
            r1 = random.randint(0,self.sudoku.dim**2-1)
            while self.sudoku.board[r1] == 0:
                r1 = random.randint(0,self.sudoku.dim**2-1)
            r2 = random.randint(0,self.sudoku.dim**2-1)
            while self.sudoku.board[r2] == 0 and r2 != r1:
                r2 = random.randint(0,self.sudoku.dim**2-1)
            aux = ind.board[r0][r1]
            ind.board[r0][r1] = ind.board[r0][r2]
            ind.board[r0][r2] = aux

    def mutation_5swap(self,ind):
        for i in range(9):
            if probabilty(self.mt_rate):
                r0 = random.randint(0,self.sudoku.dim**2-1)
                r1 = random.randint(0,self.sudoku.dim**2-1)
                while self.sudoku.board[r1] == 0:
                    r1 = random.randint(0,self.sudoku.dim**2-1)
                r2 = random.randint(0,self.sudoku.dim**2-1)
                while self.sudoku.board[r2] == 0 and r2 != r1:
                    r2 = random.randint(0,self.sudoku.dim**2-1)
                aux = ind.board[r0][r1]
                ind.board[r0][r1] = ind.board[r0][r2]
                ind.board[r0][r2] = aux

    def mutation5(self,ind):
        r = randint(0,8)
        for i in range(r):
            self.mutation_swap(ind)

    def mutation_sort(self,ind):
        if probabilty(self.mt_rate):
            r = random.randint(0,self.sudoku.dim**2-1)
            random.shuffle(ind.board[r])


    def crossover(self,ind1, ind2):
        new_ind1 = copy.deepcopy(ind1)
        new_ind2 = copy.deepcopy(ind2)
        for i, row in enumerate(new_ind1.board):
            if probabilty(self.cx_rate):
                aux = copy.deepcopy(new_ind1.board[i])
                new_ind1.board[i] = copy.deepcopy(new_ind2.board[i])
                new_ind2.board[i] = copy.deepcopy(aux)
        return (new_ind1, new_ind2)

    def selection(self):
        tot = sum([ind.fitness for ind in self.pop])
        r = random.randint(0,tot)
        cur = 0
        for ind in self.pop:
            cur += ind.fitness
            if cur > r:
                return ind
        return self.pop[len(self.pop)-1]


    def calculate_population_fitness(self):
        for ind in self.pop:
            ind.calculate_fitness()

    def aging(self,ind):
        ind.fitness = ind.fitness + 1


    def evolve(self):
        self.start_pop()
        self.calculate_population_fitness()
        self.pop.sort(key = lambda ind: ind.fitness)
        gen = 1
        best_fit = 999
        best_count = 1
        while self.pop[0].fitness != 0:
            new_pop = []
            self.calculate_population_fitness()
            self.pop.sort(key = lambda ind: ind.fitness)
            if self.pop[0].fitness < best_fit:
                best_fit = self.pop[0].fitness
                best_count = gen
            if gen - best_count >= 80:
                #print "mutated"
                best_count =gen
            #print "Generation: ", gen, " Fittest: ", self.pop[0].fitness
            if(self.pop[0].fitness == 0):
                break
            while len(new_pop) < self.pop_size:
                ind1 = self.selection()
                ind2 = self.selection()
                new_ind = self.crossover(ind1, ind2)
                self.mutation_swap(new_ind[0])
                self.mutation_swap(new_ind[1])
                new_pop.append(new_ind[0])
                new_pop.append(new_ind[1])
            new_pop.sort(key = lambda ind: ind.fitness)
            new_pop = new_pop[0:900]
            self.pop = self.pop[0:100]
            self.pop = self.pop + new_pop
            gen +=1
        print gen



def probabilty(prob):
    r = random.random()
    return  r <= prob



sdk = Sudoku(3)
ga = GA(sdk,0.3,0.5,5000)
ga.evolve()
ga.pop[0].display()
