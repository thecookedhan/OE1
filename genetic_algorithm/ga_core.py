from classes import Population
from ga_operators import *
import random
import numpy as np

def michalewicz(x, m=10):
    x = np.array(x)
    i = np.arange(1, len(x) + 1)

    return -np.sum(
        np.sin(x) *
        (np.sin(i * x**2 / np.pi)) ** (2*m)
    )

class GeneticAlgorithm:
    def __init__(self, population_size, number_of_genertions, fitness_function, bounds, bits_per_variable, number_of_variables, 
                 selection_method="tournament", mutation_method="bit_flip", crossover_method="one_point",
                 mutation_rate=0.01, tournament_size=3):
        self.population_size = population_size
        self.number_of_generations = number_of_genertions

        self.fitness_function = fitness_function
        self.bounds = bounds
        self.bits_per_variable = bits_per_variable
        self.number_of_variables = number_of_variables

        self.selection_method = selection_method
        self.mutation_method = mutation_method
        self.crossover_method = crossover_method

        self.mutation_rate = mutation_rate
        self.tournament_size = tournament_size

        self.population = Population(population_size)

        self.best_individual = None
        self.worst_individual = None
        self.average_individual = None

        self.best_fitness_history = []
        self.worst_fitness_history = []
        self.average_fitness_history = []

    def initialize_population(self):
        genome_length = self.bits_per_variable * self.number_of_variables
        self.population.initialize(genome_length)

    def evaluate_population(self):
        self.population.evaluate(self.fitness_function, self.bounds, self.bits_per_variable)

    def select_parents(self):
        if self.selection_method == "tournament":
            parent1 = tournament_selection(self.population, self.tournament_size)
            parent2 = tournament_selection(self.population, self.tournament_size)

        elif self.selection_method == "roulette":
            parent1 = roulette_selection(self.population)
            parent2 = roulette_selection(self.population)

        elif self.selection_method == "best":
            selected_individuals = best_selection(self.population)

            parent1 = random.choice(selected_individuals)
            parent2 = random.choice(selected_individuals)

        else:
            raise ValueError("Unknown selection method")

        return parent1, parent2

    def crossover(self, parent1, parent2):
        if self.crossover_method == "one_point":
            child1, child2 = one_point_crossover(parent1, parent2)

        elif self.crossover_method == "two_point":
            child1, child2 = two_point_crossover(parent1, parent2)

        elif self.crossover_method == "uniform":
            child1, child2 = uniform_crossover(parent1, parent2)

        elif self.crossover_method == "discrete":
            child1 = discrete_crossover(parent1, parent2)
            child2 = discrete_crossover(parent2, parent1)

        else:
            raise ValueError("Unknown crossover method")
        
        return child1, child2

    def mutate(self, individual):
        if self.mutation_method == "bit_flip":
            bit_flip_mutation(individual, self.mutation_rate)

        elif self.mutation_method == "two_bits":
            two_bits_flip_mutation(individual)

        elif self.mutation_method == "edge":
            edge_mutation(individual)

        else:
            raise ValueError("Unknown mutation method")

    def create_new_population(self):
        new_population = Population(self.population_size)

        while len(new_population) < self.population_size:
            parent1, parent2 = self.select_parents()
            child1, child2 = self.crossover(parent1, parent2)

            self.mutate(child1)
            self.mutate(child2)

            new_population.add_individual(child1)

            if len(new_population) < self.population_size:
                new_population.add_individual(child2)

        self.population = new_population

    def run(self):
        self.initialize_population()
        self.evaluate_population()

        self.update_best_solution()
        #self.update_worst_solution()
        #self.update_average_solution()

        for generation in range(self.number_of_generations):
            self.create_new_population()
            self.evaluate_population()

            self.update_best_solution()
            #self.update_worst_solution()
            #self.update_average_solution()

    def update_best_solution(self):
        best_in_generation = self.population.get_best_individual()

        if self.best_individual is None:
            self.best_individual = best_in_generation.copy()

        elif best_in_generation.fitness < self.best_individual.fitness:
            self.best_individual = best_in_generation.copy()

        self.best_fitness_history.append(self.best_individual.fitness)

    def update_worst_solution():
        pass

    def update_average_solution():
        pass