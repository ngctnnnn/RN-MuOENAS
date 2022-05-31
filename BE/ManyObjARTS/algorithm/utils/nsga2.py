import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np
from algorithm import Algorithm
from pymoo.pymoo.factory import get_performance_indicator
from pymoo.pymoo.algorithms.base.genetic import GeneticAlgorithm
from pymoo.pymoo.algorithms.moo.nsga2 import NSGA2

class NSGAII(NSGA2):
    def __init__(self, api, pareto_front_url, flops_log_url, proxy_log):
        super().__init__()
        self.api = api
        self.archive_phenotype = []
        self.archive_genotype = []
        self.generation_count = 0

        self.seed = 0
        self.dataset = ""
        self.pareto_front = np.genfromtxt(pareto_front_url, delimiter=',')
        self.flops_log = flops_log_url
        self.pareto_front_normalize = self.pareto_front.copy()
        self.pareto_front_normalize[:, 0] = (self.pareto_front_normalize[:, 0] - self.flops_log.min()) / (self.flops_log.max() - self.flops_log.min())
        self.pareto_front_normalize[:, 1] = self.pareto_front_normalize[:, 1] / 100
        self.res_of_run = dict()
        
    