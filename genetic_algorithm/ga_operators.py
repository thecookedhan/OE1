from classes import Individual
from classes import Population
import random

# === MUTATION ===
def bit_flip_mutation(individual: Individual, mutation_rate: float = 0.01):
    for locus in range(len(individual)):
        if random.random() < mutation_rate:
            individual.genome[locus] = 1 - individual.genome[locus]
    
    individual.fitness = None

def two_bits_flip_mutation(individual: Individual):
    random_indexes = random.sample(range(len(individual)), 2)

    individual.genome[random_indexes[0]] = 1 - individual.genome[random_indexes[0]]
    individual.genome[random_indexes[1]] = 1 - individual.genome[random_indexes[1]]

    individual.fitness = None

def edge_mutation(individual: Individual):
    individual.genome[0] = 1 - individual.genome[0]
    individual.genome[-1] = 1 - individual.genome[-1]

    individual.fitness = None

# === SELECTION ===
def tournament_selection(population: Population, tournament_size: int = 3) -> Individual:
    tournament_group = random.sample(population.individuals, tournament_size)
    best_individual = max(tournament_group, key=lambda individual: individual.fitness)

    return best_individual.copy()

def best_selection(population: Population, best_percentage: float = 0.3):
    population.sort(descending = True)
    best_individuals_start_index = int(len(population) * best_percentage)
    return [individual.copy() for individual in population.individuals[:best_individuals_start_index]]

def roulette_selection(population: Population) -> Individual:
    population_fitness_sum = sum([1/individual.fitness for individual in population])
    random_fitness = random.uniform(0, population_fitness_sum)

    cumulative_fintess_sum = 0
    for individual in population.individuals:
        cumulative_fintess_sum += individual.fitness
        if cumulative_fintess_sum >= random_fitness:
            return individual.copy()

# === CROSSOVER ===
def one_point_crossover(parent1: Individual, parent2: Individual):
    crossover_point = random.randint(0, len(parent1) - 1)

    child1_genome = parent1.genome[:crossover_point] + parent2.genome[crossover_point:]
    child2_genome = parent2.genome[:crossover_point] + parent1.genome[crossover_point:]

    return Individual(child1_genome), Individual(child2_genome)

def two_point_crossover(parent1: Individual, parent2: Individual):
    crossover_points = sorted(random.sample(range(len(parent1)), 2))

    child1_genome = parent1.genome[:crossover_points[0]] + parent2.genome[crossover_points[0]:crossover_points[1]] + parent1.genome[crossover_points[1]:]
    child2_genome = parent2.genome[:crossover_points[0]] + parent1.genome[crossover_points[0]:crossover_points[1]] + parent2.genome[crossover_points[1]:]

    return Individual(child1_genome), Individual(child2_genome)

def discrete_crossover(parent1: Individual, parent2: Individual) -> Individual:
    child_genome = []

    for locus in range(0, len(parent1)):
        if random.random() <= 0.5:
            child_genome.append(parent1.genome[locus])
        else:
            child_genome.append(parent2.genome[locus])
    
    return Individual(child_genome)

def uniform_crossover(parent1: Individual, parent2: Individual, crossover_rate: float = 0.1):
    child1_genome = []
    child2_genome = []

    for locus in range(0, len(parent1)):
        if random.random() < crossover_rate:
            child1_genome.append(parent1.genome[locus])
            child2_genome.append(parent2.genome[locus])
        else:
            child1_genome.append(parent2.genome[locus])
            child2_genome.append(parent1.genome[locus])
    
    return Individual(child1_genome), Individual(child2_genome)