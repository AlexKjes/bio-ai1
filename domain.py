import numpy as np


def truck_load(truck_route, problem):




def generate_random_population(problem, size):

    population = []
    max_trucks = problem.n_trucks_per_depot*problem.depots.shape[0]
    max_capacity = np.max(problem.depots[:, 2])
    n_customers = problem.customers.shape[0]

    route = np.sort(problem.customers[:, 3])
    max_route = 0
    n = 0
    for i, s in enumerate(route):
        n += s
        if n > max_capacity:
            max_route = i-1
            break

    for i in range(size):

        specimen = np.zeros((max_trucks, max_route))-1
        for j, c in enumerate(problem.customers):
            rand = np.arange(0, max_trucks)
            np.random.shuffle(rand)
            for t in rand:
                print(specimen[t][specimen[t] != -1].shape)
                truck_custom = specimen[t][specimen[t] != -1]
                load = np.sum(problem.customers[truck_custom]) if truck_custom.shape[0] + c[4] else 0
                if load <= max_route:
                    specimen[t, np.where(specimen[t] == -1)] = j

        print(specimen)
        input()

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
                'route': np.reshape(stop_sort, stops.shape)
            }
            trucks.append(truck)

    return trucks

def fitness_fn(problem, population):
    fit_temp = np.zeros((len(population), 2))
    for i, specimen in enumerate(population):

        for j, truck in enumerate(encode(specimen, problem)):

            depot = problem.depots[truck['depot']]
            load = depot.truck_capacity
            pos = depot.coords
            distance = 0
            for c in truck['route']:

                customer = problem.customers[c]
                distance += np.sqrt((pos[0] - customer.coords[0])**2 * (pos[1] - customer.coords[1])**2)

                pos = customer.coords
                load -= customer.demand

            distance += np.sqrt((pos[0] - depot.coords[0])**2 * (pos[1] - depot.coords[1])**2)
            fit_temp[i][0] += distance
            fit_temp[i][1] += load*(-1) if load < 0 else 0


    f_max = np.max(fit_temp, axis=0)
    f_max[f_max == 0] = 1
    f_max[0] *= 10
    normal_fit = fit_temp/f_max
    normal_fit = np.sum(normal_fit, axis=1)

    return normal_fit



def crossover(parent, truck_mut_rate=.01, route_mut_rate=.1):

    child = {'depots': np.copy(parent['depots']),
             'route': np.copy(parent['route']),
             'fitness': -1}

    rand = np.random.rand(parent['depots'].shape[0]) < truck_mut_rate
    child['depots'][rand] = (child['depots'][rand]-1)*-1

    rand = np.random.rand(parent1['route'].shape[0])
    for i, (p1, p2) in enumerate(zip(parent1['route'], parent2['route'])):
        child['route'][i] = p1 if rand[i] > .5 else p2

    return child


def generate_next_generation(population, elitism=0):

    next_population = []

    pf_sum = 0
    for s in population:
        pf_sum += s['fitness']

    while len(next_population) < (len(population)-elitism):

        rand = np.sort(np.random.rand(2)*pf_sum)
        acc = 0
        p1 = None
        for s in population:
            acc += s['fitness']
            if acc >= rand[0] and p1 is None:
                p1 = s
            elif acc >= rand[1]:
                next_population.append(crossover(p1, s))
                break

    sorted(population, key=lambda x: x['fitness'])

    for i in range(elitism):
        next_population.append(population[i])

    return next_population
