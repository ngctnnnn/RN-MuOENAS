import os, sys
from collections import namedtuple
from NASBench.NASBench import NASBench
import torch
import numpy as np 
from ConfigSpace.read_and_write import json as cs_json
import nasbench301 as nb
from graphviz import Digraph
from random import choice


def random_connection( num_individuals ):
    connection0 = np.random.randint(2, size=(num_individuals, 2))
    connection1 = np.random.randint(3, size=(num_individuals, 2))
    connection2 = np.random.randint(4, size=(num_individuals, 2))
    connection3 = np.random.randint(5, size=(num_individuals, 2))
    connection = np.concatenate((connection0, connection1, connection2, connection3), axis=1)
    return connection

def repair_ind ( ind ):
    num = 1
    for i in range(9, len(ind) // 2, 2):
        num += 1
        if (ind[i] == ind[i - 1]):
            exclude_value = ind[i - 1]
            ind[i] = choice([j for j in range(num) if j not in [exclude_value]])
        
        if (ind[i + 16] == ind[i + 15]):
            exclude_value = ind[i + 15]
            ind[i + 16] = choice([j for j in range(num) if j not in [exclude_value]])
            
    return ind


class NAS301(NASBench):
    def __init__(self):
        super().__init__()
        
        """
        Set up 301
        """
        version = '1.0'
        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        url = os.path.dirname(__file__)
        current_dir = f"{url[:-len('/NASBench')] + '/source/nasbench301/'}"
                    
        models_0_9_dir = os.path.join(current_dir, 'nb_models_0.9')
        model_paths_0_9 = {
            model_name : os.path.join(models_0_9_dir, '{}_v0.9'.format(model_name))
            for model_name in ['xgb', 'gnn_gin', 'lgb_runtime']
        }
        models_1_0_dir = os.path.join(current_dir, 'nb_models_1.0')
        model_paths_1_0 = {
            model_name : os.path.join(models_1_0_dir, '{}_v1.0'.format(model_name))
            for model_name in ['xgb', 'gnn_gin', 'lgb_runtime']
        }

        self.model_path = model_paths_0_9 if version == '0.9' else model_paths_1_0

        if not all(os.path.exists(model) for model in self.model_path.values()):
            nb.download_models(version=version, delete_zip=True, download_dir=current_dir)
        
        self.op_names = ["max_pool_3x3",
                        "avg_pool_3x3",
                        "skip_connect",
                        "sep_conv_3x3",
                        "sep_conv_5x5",
                        "dil_conv_3x3",
                        "dil_conv_5x5"]
        
    def convert_individual_to_query(self, ind):
        ind = repair_ind(ind)
        normals = []
        reduces = []
        for i in range(len(ind) // 4):
            element_normal = (self.op_names[ind[i]], ind[i + 8])
            normals.append(element_normal)
            element_reduce = (self.op_names[ind[i + 16]], ind[i + 24])
            reduces.append(element_reduce)
        
        Genotype = namedtuple('Genotype', 
                            'normal normal_concat reduce reduce_concat')
        self.cell = Genotype(
            normal=normals,
            normal_concat=list(range(2, 6)),
            reduce=reduces,
            reduce_concat=list(range(2, 6))
        )
    
    def query_bench(self, ind, model_predictor='lgb_runtime', returnGenotype=False):
        """
        Arguments
        model_predictor (optional) -- choose ensemble model (default: 'lgb_runtime', 'xgb', 'gnn_gin')
        returnGenotype (optional) -- return individual's genotype or not (default: False)
        """
        
        self.convert_individual_to_query(ind)
        
        ensemble_dir_performance = self.model_path[model_predictor]
        self.api = nb.load_ensemble(ensemble_dir_performance)
        self.query_result = self.api.predict(config=self.cell, representation="genotype", with_noise=False)
        return self.query_result if not returnGenotype else (self.query_result, self.cell)
