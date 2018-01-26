import re


class Customer:

    def __init__(self, num, coords, demand):

        self.num = num
        self.coords = coords
        self.demand = demand


class Depot:

    def __init__(self):

        self.coords = (0, 0)
        self.truck_capacity = 0

class MDVRP:

    def __init__(self):

        self.n_trucks_per_depot = 0
        self.customers = []
        self.depots = []


def read_data_file(location):

    problem = MDVRP()

    n_customers = 0
    n_depots = 0

    with open(location, "r") as f:
        for i, line in enumerate(f):
            line = line.strip(' \n')
            l = re.split(' +', line)
            if i == 0:
                problem.n_trucks_per_depot = int(l[0])
                n_customers = int(l[1])
                n_depots = int(l[2])
                for j in range(n_depots):
                    problem.depots.append(Depot())
            elif i < n_depots+1:
                problem.depots[i-1].truck_capasity = l[1]
            elif i < 1+n_depots+n_customers:
                problem.customers.append(Customer(l[0], (l[1], l[2]), l[3]))
            else:
                problem.depots[i-n_customers-n_depots-1].coords = (l[1], l[2])


    return problem
