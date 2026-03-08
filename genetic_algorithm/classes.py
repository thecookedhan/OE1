import random

class Individual:
    def __init__(self, genome: list[int], fitness: float = None): # create new Individual with binary list that represents a solution
        if not genome:
            raise ValueError("Genome cannot be empty")

        self.genome = genome
        self.fitness = fitness

    def decode(self, bounds: list[float], bits_per_variable: int) -> float: # decode biniary solution list into float in a given bounds
        decimal_genome = []

        genome_splitted_by_variables = [self.genome[i:i + bits_per_variable] for i in range(0, len(self.genome), bits_per_variable)]
        for i, variable_genome in enumerate(genome_splitted_by_variables):
            decimal_variable_genome = int(''.join(map(str, variable_genome)), 2)
            decimal_variable_genome = bounds[0] + (decimal_variable_genome / (2**bits_per_variable - 1) * (bounds[1] - bounds[0]))
            decimal_genome.append(decimal_variable_genome)

        return decimal_genome

    def evaluate(self, fitness_function, bounds: list[float], bits_per_variable: int): # calculate fitness function value based on a decoded solution list
        decoded_genome = self.decode(bounds, bits_per_variable)
        self.fitness = fitness_function(decoded_genome)

    def copy(self) -> Individual: # create copy of a individual
        return Individual(self.genome.copy(), self.fitness)

    def __len__(self) -> int: # return length of a binary solution list
        return len(self.genome)

    def __repr__(self) -> str: # return ready to print string with individual atributes
        return f'Individual(genome = {self.genome}, fitness = {self.fitness})'
    
class Population:
    def __init__(self, population_size: int, individuals: list[Individual] = None): # get input population size or create population when list of individuals is given
        if individuals is None:
            self.individuals = []
        else:
            self.individuals = individuals
        
        if population_size <= 0:
            raise ValueError("Population size must be positive")
        self.population_size = population_size

    def initialize(self, genome_length: int): # create new population filled with individuals with given solution accuracy/length
        self.clear()

        for _ in range(self.population_size):
            genome = [random.randint(0, 1) for _ in range(genome_length)]
            self.add_individual(Individual(genome))

    def evaluate(self, fitness_function, bounds: list[float], bits_per_variable: int): # calculate fitness function value based on a decoded solution list for a whole population
        for individual in self.individuals:
            individual.evaluate(fitness_function, bounds, bits_per_variable)

    def get_best_individual(self) -> Individual: # return an individual which has the best solution in a population
        return min(self.individuals, key=lambda ind: ind.fitness)
    
    def get_worst_individual(self) -> Individual: # return an individual which has the worst solution in a population
        return max(self.individuals, key=lambda ind: ind.fitness)

    def add_individual(self, individual: Individual): # add a single new individual to a population
        self.individuals.append(individual)

    def extend(self, individuals_list: list[Individual]): # extend population with list of a new individuals
        self.individuals.extend(individuals_list)

    def clear(self): # clear population
        self.individuals = []

    def sort(self, descending: bool): # sort population by fitness value in descending/ascending order
        self.individuals.sort(key = lambda ind: ind.fitness, reverse = descending)

    def __len__(self) -> int: # return population length, which is simply a number of individuals in a population
        return len(self.individuals)
    
    def __repr__(self) -> str: # return ready to print string with population atributes
        return f'Population(individuals = {self.individuals}, size = {self.population_size})'