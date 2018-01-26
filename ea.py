




class EvolutionaryAlgorithm:

    def __init__(self, population_size, mutation_rate, crossover_fn, fitness_fn):

        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_fn
        self.fitness_fn = fitness_fn
        self.generation_n = 0

        self.population = []
