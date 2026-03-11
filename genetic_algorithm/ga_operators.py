from classes import Individual
from classes import Population
import random

# === MUTATION ===
def bit_flip_mutation(individual: Individual, bit_mutation_rate: float): # randomly inverse each bit in individual's genome (binary solution list)
    for locus in range(len(individual)):
        if random.random() < bit_mutation_rate:
            individual.genome[locus] = 1 - individual.genome[locus]
    
    individual.fitness = None

def two_bits_flip_mutation(individual: Individual): # randomly inverse exactly two bits in the individual's genome (binary solution list)
    random_indexes = random.sample(range(len(individual)), 2)

    individual.genome[random_indexes[0]] = 1 - individual.genome[random_indexes[0]]
    individual.genome[random_indexes[1]] = 1 - individual.genome[random_indexes[1]]

    individual.fitness = None

def edge_mutation(individual: Individual): # inverse the first and the last bit in the individual's genome (binary solution list)
    individual.genome[0] = 1 - individual.genome[0]
    individual.genome[-1] = 1 - individual.genome[-1]

    individual.fitness = None

def inversion_mutation(individual: Individual, max_segment_ratio: float): # reverse a random segment of the individual's genome (binary solution list)
    max_segment = int(len(individual) * max_segment_ratio)

    start = random.randint(0, len(individual) - max_segment)
    end = start + random.randint(2, max_segment)

    individual.genome[start:end] = reversed(individual.genome[start:end])

    individual.fitness = None

# === SELECTION ===
def tournament_selection(population: Population, tournament_size: int) -> Individual: # select the best individual from a random subset of the population based on fitness
    tournament_group = random.sample(population.individuals, tournament_size)
    best_individual = min(tournament_group, key=lambda individual: individual.fitness)

    return best_individual.copy()

def best_selection(population: Population, best_percentage: float) -> Individual: # select a percentage of the best individuals from the population based on fitness
    population.sort(descending = True)
    best_individuals_start_index = int(len(population) * best_percentage)

    return random.choice(population.individuals[:best_individuals_start_index]).copy()

def roulette_selection(population: Population) -> Individual: # select an individual with probability proportional to its fitness
    min_population_fitness = min(individual.fitness for individual in population.individuals)
    shift = abs(min_population_fitness) + 1e-6

    population_fitness_sum = sum([1 / (individual.fitness + shift) for individual in population.individuals])
    random_fitness = random.uniform(0, population_fitness_sum)

    cumulative_fintess_sum = 0
    for individual in population.individuals:
        cumulative_fintess_sum += 1 / (individual.fitness + shift)
        if cumulative_fintess_sum >= random_fitness:
            return individual.copy()

# === CROSSOVER ===
def one_point_crossover(parent1: Individual, parent2: Individual): # create two children (new individuals) by exchanging parent's (population individuals) genomes parts at one random point
    crossover_point = random.randint(0, len(parent1) - 1)

    child1_genome = parent1.genome[:crossover_point] + parent2.genome[crossover_point:]
    child2_genome = parent2.genome[:crossover_point] + parent1.genome[crossover_point:]

    return Individual(child1_genome), Individual(child2_genome)

def two_point_crossover(parent1: Individual, parent2: Individual): # create two children by exchanging genome segments between two points
    crossover_points = sorted(random.sample(range(len(parent1)), 2))

    child1_genome = parent1.genome[:crossover_points[0]] + parent2.genome[crossover_points[0]:crossover_points[1]] + parent1.genome[crossover_points[1]:]
    child2_genome = parent2.genome[:crossover_points[0]] + parent1.genome[crossover_points[0]:crossover_points[1]] + parent2.genome[crossover_points[1]:]

    return Individual(child1_genome), Individual(child2_genome)

def discrete_crossover(parent1: Individual, parent2: Individual) -> Individual: # create a child by randomly choosing each gene from one of the parents
    child_genome = []

    for locus in range(0, len(parent1)):
        if random.random() <= 0.5:
            child_genome.append(parent1.genome[locus])

        else:
            child_genome.append(parent2.genome[locus])
    
    return Individual(child_genome)

def uniform_crossover(parent1: Individual, parent2: Individual, crossover_rate: float): # create two children by randomly swapping genes between parents
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