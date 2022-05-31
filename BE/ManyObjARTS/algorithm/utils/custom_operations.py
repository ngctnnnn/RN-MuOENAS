import os, sys 
import numpy as np

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pymoo.pymoo.operators.crossover.pntx import PointCrossover
from pymoo.pymoo.core.crossover import Crossover
from pymoo.pymoo.operators.crossover.util import crossover_mask
from pymoo.pymoo.operators.mutation.pm import PolynomialMutation
from pymoo.pymoo.operators.repair.to_bound import set_to_bounds_if_outside_by_problem

# from NASBench.NAS101 import NAS101 

# nasbench101_api = NAS101(debug=True)
 
class CustomUniformCrossover(Crossover):
    def __init__(self, **kwargs):
        super().__init__(n_parents=2, n_offsprings=2, **kwargs)

    def _do(self, _, X, api, **kwargs):
        _, n_matings, n_var = X.shape
        parents = X.copy()
        cnt = 0
        np.random.seed(cnt)
        
        M = np.random.random((n_matings, n_var)) < 0.5
        _X = crossover_mask(X, M)
        if api.is_valid(_X[0]) and api.is_valid(_X[1]):
            return _X
        else:
            maximum_crossover_operations = len(_X[0])
            cnt += 1
            while True:
                M = np.random.random((n_matings, n_var)) < 0.5
                np.random.seed(cnt) 
                _X = crossover_mask(X, M) 
                
                if api.is_valid(_X[0]) and api.is_valid(_X[1]):
                    break

                if cnt == maximum_crossover_operations:
                    _X = parents 
                    break
                
                cnt += 1
        return _X

    
class CustomPolynomialMutation(PolynomialMutation):
    def __init__(self, eta, prob=0.0):
        super().__init(eta=eta, prob=prob)
        
    def _do(self, problem, X):
        X = X.astype(float)
        Y = np.full(X.shape, np.inf)

        if self.prob is None:
            self.prob = 1.0 / problem.n_var

        do_mutation = np.random.random(X.shape) < self.prob

        Y[:, :] = X

        xl = np.repeat(problem.xl[None, :], X.shape[0], axis=0)[do_mutation]
        xu = np.repeat(problem.xu[None, :], X.shape[0], axis=0)[do_mutation]

        X = X[do_mutation]

        delta1 = (X - xl) / (xu - xl)
        delta2 = (xu - X) / (xu - xl)

        mut_pow = 1.0 / (self.eta + 1.0)

        rand = np.random.random(X.shape)
        mask = rand <= 0.5
        mask_not = np.logical_not(mask)

        deltaq = np.zeros(X.shape)

        xy = 1.0 - delta1
        val = 2.0 * rand + (1.0 - 2.0 * rand) * (np.power(xy, (self.eta + 1.0)))
        d = np.power(val, mut_pow) - 1.0
        deltaq[mask] = d[mask]

        xy = 1.0 - delta2
        val = 2.0 * (1.0 - rand) + 2.0 * (rand - 0.5) * (np.power(xy, (self.eta + 1.0)))
        d = 1.0 - (np.power(val, mut_pow))
        deltaq[mask_not] = d[mask_not]

        # mutated values
        _Y = X + deltaq * (xu - xl)

        # back in bounds if necessary (floating point issues)
        _Y[_Y < xl] = xl[_Y < xl]
        _Y[_Y > xu] = xu[_Y > xu]

        # set the values for output
        Y[do_mutation] = _Y

        # in case out of bounds repair (very unlikely)
        Y = set_to_bounds_if_outside_by_problem(problem, Y)

        return Y