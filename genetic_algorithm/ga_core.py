from classes import Population
from ga_operators import *
import random
import numpy as np

class GeneticAlgorithm:
    def __init__(self, population_size: int, number_of_genertions: int, fitness_function, bounds: list[float], bits_per_variable: int, number_of_variables: int, 
                 selection_method: str = "tournament", tournament_size: int = 3, mutation_method:str = "bit_flip", mutation_probability: float = 0.2, bit_mutation_rate: float = 0.01, 
                 max_segment_ratio: float = 0.3, crossover_method: str = "one_point", crossover_probability: float = 0.75, uniform_crossover_rate: float = 0.1, elitism_size: int = 0, best_percentage: float = 0.05): # initialize genetic algorithm parameters, operators and population
        self.population_size = population_size
        self.number_of_generations = number_of_genertions

        self.fitness_function = fitness_function
        self.bounds = bounds
        self.bits_per_variable = bits_per_variable
        self.number_of_variables = number_of_variables

        self.selection_method = selection_method
        self.tournament_size = tournament_size

        self.mutation_method = mutation_method
        self.mutation_probability = mutation_probability
        self.bit_mutation_rate = bit_mutation_rate
        self.max_segment_ratio = max_segment_ratio

        self.crossover_method = crossover_method
        self.crossover_probability = crossover_probability
        self.uniform_crossover_rate = uniform_crossover_rate
        
        self.best_percentage = best_percentage
        self.elitism_size = elitism_size

        self.population = Population(population_size)

        self.best_individual = None
        self.worst_individual = None
        self.median_individual = None

        self.best_fitness_history = []
        self.worst_fitness_history = []
        self.median_fitness_history = []

    def initialize_population(self): # create initial population with random genomes (binary solution lists)
        genome_length = self.bits_per_variable * self.number_of_variables
        self.population.initialize(genome_length)

    def evaluate_population(self): # compute fitness function value for every individual in the population
        self.population.evaluate(self.fitness_function, self.bounds, self.bits_per_variable)

    def select_parents(self): # select two individuals from the population using the chosen selection method
        if self.selection_method == "tournament":
            parent1 = tournament_selection(self.population, self.tournament_size)
            parent2 = tournament_selection(self.population, self.tournament_size)

        elif self.selection_method == "roulette":
            parent1 = roulette_selection(self.population)
            parent2 = roulette_selection(self.population)

        elif self.selection_method == "best":
            parent1 = best_selection(self.population, self.best_percentage)
            parent2 = best_selection(self.population, self.best_percentage)

        else:
            raise ValueError("Unknown selection method")

        return parent1, parent2

    def crossover(self, parent1: Individual, parent2: Individual): # generate new individuals using the selected crossover operator
        if random.random() > self.crossover_probability:
            return parent1.copy(), parent2.copy()
    
        if self.crossover_method == "one_point":
            child1, child2 = one_point_crossover(parent1, parent2)

        elif self.crossover_method == "two_point":
            child1, child2 = two_point_crossover(parent1, parent2)

        elif self.crossover_method == "uniform":
            child1, child2 = uniform_crossover(parent1, parent2, self.uniform_crossover_rate)

        elif self.crossover_method == "discrete":
            child1 = discrete_crossover(parent1, parent2)
            child2 = discrete_crossover(parent2, parent1)

        else:
            raise ValueError("Unknown crossover method")
        
        return child1, child2

    def mutate(self, individual: Individual): # apply selected mutation operator to a single individual
        if random.random() > self.mutation_probability:
            return
    
        if self.mutation_method == "bit_flip":
            bit_flip_mutation(individual, self.bit_mutation_rate)

        elif self.mutation_method == "two_bits":
            two_bits_flip_mutation(individual)

        elif self.mutation_method == "edge":
            edge_mutation(individual)

        elif self.mutation_method == "inversion":
            inversion_mutation(individual, self.max_segment_ratio)

        else:
            raise ValueError("Unknown mutation method")

    def create_new_population(self): # generate a new population using selection, crossover and mutation
        new_population = Population(self.population_size)

        if self.elitism_size > 0:
            elites = sorted(self.population.individuals, key=lambda ind: ind.fitness)[:self.elitism_size]

            for elite in elites:
                new_population.add_individual(elite.copy())

        while len(new_population) < self.population_size:
            parent1, parent2 = self.select_parents()
            child1, child2 = self.crossover(parent1, parent2)

            self.mutate(child1)
            self.mutate(child2)

            new_population.add_individual(child1)

            if len(new_population) < self.population_size:
                new_population.add_individual(child2)

        self.population = new_population

    def run(self): # execute the genetic algorithm for the specified number of generations
        self.initialize_population()
        self.evaluate_population()

        self.update_best_solution()
        self.update_worst_solution()
        self.update_median_solution()

        for _ in range(self.number_of_generations):
            self.create_new_population()
            self.evaluate_population()

            self.update_best_solution()
            self.update_worst_solution()
            self.update_median_solution()

    def update_best_solution(self): # track and save fitness value of the best individual found so far in the population
        best_in_generation = self.population.get_best_individual()

        if self.best_individual is None:
            self.best_individual = best_in_generation.copy()

        elif best_in_generation.fitness < self.best_individual.fitness:
            self.best_individual = best_in_generation.copy()

        self.best_fitness_history.append(self.best_individual.fitness)

    def update_worst_solution(self): # track and save fitness value of the worst individual found so far in the population
        worst_in_generation = self.population.get_worst_individual()

        if self.worst_individual is None:
            self.worst_individual = worst_in_generation.copy()

        elif worst_in_generation.fitness < self.worst_individual.fitness:
            self.worst_individual = worst_in_generation.copy()
        
        self.worst_fitness_history.append(self.worst_individual.fitness)

    def update_median_solution(self): # track and save fitness value of the median individual found so far in the population
        median_in_generation = self.population.get_median_individual()

        if self.median_individual is None:
            self.median_individual = median_in_generation.copy()

        elif median_in_generation.fitness < self.median_individual.fitness:
            self.median_individual = median_in_generation.copy()
        
        self.median_fitness_history.append(self.median_individual.fitness)