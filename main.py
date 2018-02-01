import data_reader
import domain
import numpy as np


prob = data_reader.read_data_file('Testing Data/Data Files/p01')
popu = domain.generate_random_population(prob, 100)

print(popu[0])
print(domain.row_inverse_mutate(popu[0]))

input()

while True:

    fitness = domain.fitness_fn(prob, popu)
    print("Mean: {0}\tmin: {1}".format((np.mean(fitness)), np.min(fitness)))
    popu = domain.generate_next_generation(prob, popu, fitness, 5)
    #popu = domain.generate_next_generation(popu, 4)

