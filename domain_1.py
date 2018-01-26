


class Population:

    def __init__(self, problem, size):

        self.problem = problem


class Car:

    def __init__(self, depot, supply, route):

        self.depot = depot
        self.supply = supply
        self.route = route


class Genotype:

    def __init__(self, depots, customers, supply):

        self.depots = depots
        self.customers = customers
        self.supply = supply

class Individual:

    def __init__(self, genotype):

        self.genotype = genotype
        self.phenotype = None

    def create_phenotype(self, genotype):
        cars = []
        for i in range(len(genotype.depot)):
            cars.append(Car(genotype.depots[i], genotype.customers))

def fitness_fn(phenotype):

    fitness = 0

    for car in pthenotype