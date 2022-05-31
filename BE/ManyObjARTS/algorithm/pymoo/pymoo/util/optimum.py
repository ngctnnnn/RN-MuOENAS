import numpy as np

from pymoo.pymoo.core.individual import Individual
from pymoo.pymoo.core.population import Population
from pymoo.pymoo.util.nds.non_dominated_sorting import NonDominatedSorting


def filter_optimum(pop, least_infeasible=False):

    # if the population is none to optimum can be found
    if pop is None or len(pop) == 0:
        return None

    # first only choose feasible solutions
    ret = pop[pop.get("feasible")[:, 0]]

    # if at least one feasible solution was found
    if len(ret) > 0:

        # then check the objective values
        F = ret.get("F")

        if F.shape[1] > 1:
            I = NonDominatedSorting().do(F, only_non_dominated_front=True)
            ret = ret[I]

        else:
            ret = ret[np.argmin(F)]

    # no feasible solution was found
    else:
        # if flag enable report the least infeasible
        if least_infeasible:
            ret = pop[np.argmin(pop.get("CV"))]
        # otherwise just return none
        else:
            ret = None

    if isinstance(ret, Individual):
        ret = Population().create(ret)

    return ret