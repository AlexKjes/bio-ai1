import numpy as np


def truck_load(truck_route, problem):

    stops = truck_route[truck_route != -1]
    #print(stops)
    if stops.shape[0] == 0:
        return 0
    return np.sum(problem.customers[stops, 3])

def generate_random_population(problem, size):

    population = []
    max_trucks = problem.n_trucks_per_depot*problem.depots.shape[0]
    max_capacity = np.max(problem.depots[:, 2])
    n_customers = problem.customers.shape[0]

    # calculate max possible customers
    route = np.sort(problem.customers[:, 3])
    max_route = 0
    n = 0
    for i, s in enumerate(route):
        n += s
        if n > max_capacity:
            max_route = i-1
            break

    # distribute customers
    for i in range(size):

        specimen = np.zeros((max_trucks, max_route), dtype=np.int32)-1
        for j in range(n_customers):
            rand = np.arange(0, max_trucks)
            np.random.shuffle(rand)
            for t in rand:
                if truck_load(specimen[t], problem) + problem.customers[j][3] <= max_capacity:
                    specimen[t, np.argmin(specimen[t])] = j
                    break

        population.append(specimen)

    return population


def encode(specimen, problem):

    trucks = []

    for i, r in enumerate(specimen):
        if np.sum(r) > 0:

            stops = r[r != 0]
            sortidx = np.argsort(stops)
            stop_sort = np.argwhere(r)[sortidx]

            truck = {
                'depot': i//problem.n_trucks_per_depot,
                'route': r[r != -1]
            }
            trucks.append(truck)

    return trucks


def fitness_fn(problem, population):
    fitness = np.zeros(len(population))
    for i, specimen in enumerate(population):

        for j, truck in enumerate(encode(specimen, problem)):

            depot = problem.depots[truck['depot']]
            pos = depot[:2]
            distance = 0
            for c in truck['route']:

                customer = problem.customers[c]
                distance += np.sqrt((pos[0] - customer[0])**2 + (pos[1] - customer[1])**2)

                pos = customer[:2]

            distance += np.sqrt((pos[0] - depot[0])**2 + (pos[1] - depot[1])**2)
            fitness[i] += distance

    return fitness


def crossover(problem, parent1, parent2, crossover_rate=.1):

    child = np.zeros(parent1.shape, dtype=np.int32)-1
    taken = np.zeros(problem.customers.shape[0])

    for i in range(parent1.shape[0]):
        for j in range(parent1.shape[1]):
            if taken[parent2[i, j]] != 1 and np.random.rand(1) > crossover_rate and parent2[i, j] != -1 and \
                    (truck_load(child[i], problem) + problem.customers[parent2[i, j], 3]) < problem.depots[0][2]:

                child[i, j] = parent2[i, j]
                taken[parent2[i, j]] = 1

            elif taken[parent1[i, j]] != 1 and parent1[i, j] != -1 and \
                 (truck_load(child[i], problem) + problem.customers[parent1[i, j], 3]) < problem.depots[0][2]:

                child[i, j] = parent1[i, j]
                taken[parent1[i, j]] = 1
            else:
                break

    for i in np.where(taken==0)[0]:
        rand = np.arange(0, parent1.shape[1])
        np.random.shuffle(rand)

        for j in rand:
            if (truck_load(child[j], problem) + problem.customers[i, 3]) <= problem.depots[0, 2]:
                child[j, np.argmin(child[j])] = i
                break

    return child


def generate_next_generation(problem, population, fitness, elitism=0):

    next_population = []

    pf_sum = np.sum(fitness)
    fitness = np.max(fitness) - fitness

    while len(next_population) < (len(population)-elitism):

        rand = np.sort(np.random.rand(2)*pf_sum)
        acc = 0
        p1 = None
        for i in range(len(population)):
            acc += fitness[i]
            if acc >= rand[0] and p1 is None:
                p1 = i
            elif acc >= rand[1]:
                next_population.append(crossover(problem, population[p1], population[i]))
                break

    for i in np.argsort(fitness)[::-1][:elitism]:
        next_population.append(population[i])

    return next_population


def compliment_mutate(specimen):

    specimen = np.copy(specimen)
    specimen[specimen != -1] = np.max(specimen) - specimen[specimen != -1]
    return specimen


def row_inverse_mutate(specimen):

    specimen = np.copy(specimen)
    row_i = np.random.randint(0, specimen.shape[0])
    row = specimen[row_i]
    row_width = row[row != -1].shape[0]
    if row_width > 1:
        rmin = np.random.randint(0, row_width-1)
        rmax = np.random.randint(rmin+1, row_width)
        specimen[row_i, rmin:rmax] = specimen[row_i, rmin:rmax][::-1]
        print(row_i, rmin, rmax)
    return specimen