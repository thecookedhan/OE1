import random

class Individual:
    def __init__(self, genome: list[int], fitness = None):
        if not genome:
            raise ValueError("Genome cannot be empty")

        self.genome = genome
        self.fitness = fitness

    def decode(self, bounds, bits_per_variable):
        decimal_genome = []

        genome_splitted_by_variables = [self.genome[i:i + bits_per_variable] for i in range(0, len(self.genome), bits_per_variable)]
        for i, variable_genome in enumerate(genome_splitted_by_variables):
            decimal_variable_genome = int(''.join(map(str, variable_genome)), 2)
            decimal_variable_genome = bounds[i][0] + (decimal_variable_genome / (2**bits_per_variable - 1) * (bounds[i][1] - bounds[i][0]))
            decimal_genome.append(decimal_variable_genome)

        return decimal_genome

    def evaluate(self, fitness_function, bounds, bits_per_variable):
        decoded_genome = self.decode(bounds, bits_per_variable)
        self.fitness = fitness_function(*decoded_genome)

    def copy(self):
        return Individual(self.genome.copy(), self.fitness)

    def __len__(self):
        return len(self.genome)

    def __repr__(self):
        return f'Individual(genome = {self.genome}, fitness = {self.fitness})'
    
class Population:
    def __init__(self, population_size: int, individuals: list[Individual] = None):
        if individuals is None:
            self.individuals = []
        else:
            self.individuals = individuals
        
        if population_size <= 0:
            raise ValueError("Population size must be positive")
        self.population_size = population_size

    def initialize(self, genome_length):
        self.clear()

        for _ in range(self.population_size):
            genome = [random.randint(0, 1) for _ in range(genome_length)]
            self.add_individual(Individual(genome))

    def evaluate(self, fitness_function, bounds, bits_per_variable):
        for individual in self.individuals:
            individual.evaluate(fitness_function, bounds, bits_per_variable)

    def get_best_individual(self):
        return max(self.individuals, key=lambda ind: ind.fitness)
    
    def get_worst_individual(self):
        return min(self.individuals, key=lambda ind: ind.fitness)

    def add_individual(self, individual: Individual):
        self.individuals.append(individual)

    def extend(self, individuals_list: list[Individual]):
        self.individuals.extend(individuals_list)

    def clear(self):
        self.individuals = []

    def sort(self, descending):
        self.individuals.sort(key = lambda ind: ind.fitness, reverse = descending)

    def __len__(self):
        return len(self.individuals)
    
    def __repr__(self):
        return f'Population(individuals = {self.individuals}, size = {self.population_size})'