import re
import numpy as np

class MDVRP:

    def __init__(self, n_customers, n_depots, n_trucks_per_depot):

        self.n_trucks_per_depot = n_trucks_per_depot
        self.customers = np.zeros((n_customers, 4))
        self.depots = np.zeros((n_depots, 3))


def read_data_file(location):

    problem = None

    n_customers = 0
    n_depots = 0

    with open(location, "r") as f:
        for i, line in enumerate(f):
            line = line.strip(' \n')
            l = re.split(' +', line)
            if i == 0:
                problem = MDVRP(
                    int(l[1]),
                    int(l[2]),
                    int(l[0])
                )
                n_depots = int(l[2])
                n_customers = int(l[1])
            elif i < n_depots+1:
                problem.depots[i-1, 2] = int(l[1])
            elif i < 1+n_depots+n_customers:
                problem.customers[i-1-n_depots] = [int(l[1]), int(l[2]), int(l[3]), int(l[4])]
            else:
                problem.depots[i-n_customers-n_depots-1, :2] = (int(l[1]), int(l[2]))

    return problem
