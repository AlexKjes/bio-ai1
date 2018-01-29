import data_reader
import domain
import numpy as np


prob = data_reader.read_data_file('Testing Data/Data Files/p01')
popu = domain.generate_random_population(prob, 10)

input()

while True:

    print(domain.fitness_fn(prob, popu))
    input()
    #popu = domain.generate_next_generation(popu, 4)

