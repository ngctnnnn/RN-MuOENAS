import time
import numpy as np
from algorithm.pymoo.pymoo.core.problem import Problem
from algorithm.utils.algorithm import Algorithm
from algorithm.pymoo.pymoo.factory import get_performance_indicator
from search201 import NATSBench

class NASBench101(NATSBench):
    def __init__(self, n_var, n_obj, xl, xu, api, dataset, pareto_front_url, proxy_log):
        Problem().__init__(n_var=n_var, n_obj=n_obj, xl=xl, xu=xu)
        self.api = api
        self.archive_phenotype = []
        self.archive_genotype = []
        self.generation_count = 0
        self.dataset = dataset
        self.proxy_log = proxy_log # {'test-accuracy': '', 'flops': ''}
        
        self.pareto_front = np.genfromtxt(pareto_front_url, delimiter=',')
        self.flops_log = np.genfromtxt(proxy_log['flops'])
        self.pareto_front_normalize = self.pareto_front.copy()
        self.pareto_front_normalize[:, 0] = (self.pareto_front_normalize[:, 0] - self.flops_log.min()) / (self.flops_log.max() - self.flops_log.min())
        self.pareto_front_normalize[:, 1] = self.pareto_front_normalize[:, 1] / 100
        self.res_of_run = {
            'time': [],
            'igd': [],
            'igd_normalize': [],
            'archive_genotype': [],
            'archive_phenotype': [],
            'log_testacc_flops': [],
            'log_objectives': [],
            'log_pop': [],
            'archive_transform_2obj': [],
            'archive_transform_2obj_normalize': [],
        }
        
         
    def calc_IGD(self, pop, objectives):
        return super().calc_IGD(pop, objectives)
    
    def _evaluate(self, designs, out, *args, **kwargs):
        super()._evaluate(designs, out, *args, **kwargs)
        