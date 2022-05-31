import time
import numpy as np
from algorithm.pymoo.pymoo.core.problem import Problem
from algorithm.utils.algorithm import Algorithm
from algorithm.pymoo.pymoo.factory import get_performance_indicator
from search101 import NASBench101

class NASBench1Shot1(NASBench101):
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
        start = time.time()
        print(f'Gen: {self.generation_count}')

        objectives_names = [] # List of objectives names
        for obj in self.proxy_log:
            if obj != 'test-accuracy':
                objectives_names.append(obj)
        
        testacc = []
        objectives_result = {}
        for obj in objectives_names:
            objectives_result[obj] = []
        
        for design in designs:
            testacc.append(self.api.evaluate_arch(ind=design, dataset=self.dataset, measure='test-accuracy', epoch=200, use_csv=True, proxy_log=self.proxy_log['test-accuracy']))
            for obj in objectives_names:
                if obj in ['synflow', 'jacob_cov']:
                    objectives_result[obj].append(-1 * self.api.evaluate_arch(ind=design, dataset=self.dataset, measure=obj))
                else:
                    objectives_result[obj].append(self.api.evaluate_arch(ind=design, dataset=self.dataset, measure=obj, use_csv=True, proxy_log=self.proxy_log[obj]))
        

        objectives = np.array(objectives_result['flops'])
        for obj in objectives_names:
            if obj != 'flops':
                objectives = np.array(np.stack((objectives, np.array(objectives_result[obj])), axis=-1))
        print(f'All objectives: {objectives}')
        
        testacc_flops = np.array(np.stack((objectives_result['flops'], testacc), axis=-1))
        print(f'testacc_flops: {testacc_flops}')
        
        self.calc_IGD(pop=designs, objectives=objectives)

        out['F'] = np.array(objectives)
        end = time.time()
        elapsed_time = end - start
        print('time:', elapsed_time)

        self.res_of_run['time'].append(elapsed_time)
        self.res_of_run['log_testacc_flops'].append(testacc_flops)
        self.res_of_run['log_objectives'].append(objectives)
        self.res_of_run['log_pop'].append(designs)
        self.generation_count +=1    
        