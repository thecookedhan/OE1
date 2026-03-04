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
    def __init__(self, individuals: list[Individual], generation: int):
        self.individuals = individuals
        self.generation = generation

    def evaluate(fitness_function):
        pass

    def get_best():
        pass

    def get_worst():
        pass

    def sort(descdending=True):
        pass

    def add(individual: Individual):
        pass

    def extend(individuals: list[Individual]):
        pass

    def size(self):
        return len(self.individuals)