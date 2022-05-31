import torch
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import copy
import numpy as np
import matplotlib.pyplot as plt
import random
from NASBench.NASBench import NASBench
from ZeroCostNas.foresight.models import nasbench1
from ZeroCostNas.foresight.pruners import predictive
from ZeroCostNas.foresight.weight_initializers import init_net
from ZeroCostNas.AutoDLTools.xautodl.utils.flop_benchmark import *
from source.nasbench.nasbench import api
from ZeroCostNas.OpCounter.thop import profile

from NASBench.NAS101 import NAS101

def get_num_classes(args):
    if args.dataset == 'cifar100':
        return 100
    if args.dataset == 'cifar10':
        return 10
    if args.dataset == 'imagenet':
        return 120
    raise Exception('Unknown dataset')

class NASBench1Shot1(NAS101):
    def __init__(self, search_space, use_colab=True, debug=False):
        super().__init__(use_colab=use_colab, debug=debug)
        self.search_space = search_space
    
    # def individual_to_parents(self, ind):
    def get_individual(self, ind):
        config_space = {
            '5': [(0,), (1,)],
            '6': [(0,), (1,), (2,)],
            '7': [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)],
            '8': [(0, 1), (0, 2), (0, 3), (0, 4), (1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)],
            '9': [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (1, 2), (1, 3), (1, 4), (1, 5), (2, 3), (2, 4), (2, 5), (3, 4), (3, 5), (4, 5)]
        }
        parents = {
            '0': [],
            '1': [0]
        }
        cnt = 2
        for idx in range(5, len(ind)):
            parents[f'{cnt}'] = config_space[f'{idx}'][ind[idx]]
            cnt += 1
        matrix = self.search_space.create_nasbench_adjacency_matrix_with_loose_ends(parents)
        result = [[0 for _ in range(len(matrix[0]))] for _ in range(len(matrix))]
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                result[i][j] = int(matrix[i][j])
        return result
    
    def get_operations(self, ind):
        list_ops = {
            '0': 'conv1x1-bn-relu',
            '1': 'conv3x3-bn-relu',
            '2': 'maxpool3x3'
        }
        res = ['input']
        for idx in range(len(ind) - 5):
            res.append(list_ops[f'{ind[idx]}'])
        res.append('output')
        return res
    
    def get_architecture(self, ind):
        ops = self.get_operations(ind)
        ind = self.get_individual(ind)
        self.cell = api.ModelSpec(ind, ops)
        return self.cell 
    
    def query_bench(self, ind, ops, metric=None, epochs=108):
        """
        Arguments:
        metric (optional) --  metric to query ('module_adjacency', 
                                            'module_operations', 
                                            'trainable_parameters', 
                                            'training_time', 
                                            'train_accuracy', 
                                            'validation_accuracy', 
                                            'test_accuracy')
        """  
        self.cell = api.ModelSpec(ind, ops)
        try:
            self.query_result = self.api.query(self.cell, epochs=epochs)
        except:
            print(f"Cell {self.cell.__dict__['original_matrix']} is invalid for NASBench101")    
            self.api._check_spec(self.cell)

        return self.query_result[metric] if metric is not None else self.query_result

    def is_valid(self, ind):
        individual = self.get_individual(ind)
        ops = self.get_operations(ind)
        self.cell = api.ModelSpec(individual, ops)
        return self.api.is_valid(self.cell)

    def evaluate_arch(self, ind, measure, args=None, train_loader=None, use_csv=False, proxy_log=None, epoch=None):
        """
        Function to evaluate an architecture
        
        Arguments:
        ind -- Evaluating individual (DAG representation)
        measure -- Evaluation method ('train_accuracy',
                                    'validation_accuracy',
                                    'test_accuracy',
                                    'trainable_parameters',
                                    'training_time',
                                    'flops' - MB,
                                    'macs' - GB,
                                    'params',
                                    'synflow',
                                    'jacob_cov',
                                    'snip',
                                    'grasp',
                                    'fisher').
        args -- Argparse to pass through 
        train_loader -- Data train loader
        use_csv (optional) -- To choose whether to use csv file to get results (Bool)
        proxy_log (optional, but required if use_csv is True) -- Log file 
        epoch -- If measure is accuracy, this is the epoch to evaluate (4, 12, 36, 108)

        Returns:
        result[measure] -- Result of evaluation at the present dataset
        """
        
        ops = self.get_operations(ind)
        ind = self.get_individual(ind)
        
        self.cell = api.ModelSpec(ind, ops)
        # print(self.cell.__dict__)
         
        if use_csv and proxy_log is None:
            raise Exception("No proxy log to query csv")
        
        if ('accuracy' in measure or measure in ['training_time']) and epoch == None:
            raise Exception('No epoch to evaluate')
        
        proxy_log = {}
        
        result = {}

        # If query from csv file and exists respective log file
        if use_csv and measure in proxy_log:
            pass
        
        # If don't use log file, then evaluate directly from NASBench101
        else:
            
            # If measure is 'train_accuracy' or 'validation_accuracy' or 'test_accuracy'
            if epoch != None and ('accuracy' in measure or measure in ['training_time']):
                result[measure] = self.query_bench(ind, ops, metric=measure, epochs=epoch)
            
            elif measure in ['trainable_parameters']:
                result[measure] = self.query_bench(ind, ops, metric=measure)
            
            elif measure in ['macs', 'params']:
                if args == None:
                    raise Exception('No argparse to get MACs/#Params')

                if train_loader == None:
                    raise Exception('No train loader to get MACs/#Params')

                model = nasbench1.Network(self.cell, 
                                        stem_out=128, 
                                        num_stacks=3, 
                                        num_mods=3,
                                        num_classes=get_num_classes(args))
                
                input = torch.randn(len(train_loader), 3, 32, 32)
                result['macs'], result['params'] = profile(model, inputs=(input, ), verbose=False)
            
            elif measure == 'flops':

                if train_loader == None:
                    raise Exception('No train loader to get FLOPs')
                    
                if args == None:
                    raise Exception('No argparse to get FLOPs')
                
                input_size = 32 # CIFAR-10
                
                model = nasbench1.Network(self.cell, 
                                        stem_out=128, 
                                        num_stacks=3, 
                                        num_mods=3,
                                        num_classes=get_num_classes(args))
                result['flops'], _ = get_model_infos(model, (len(train_loader), 3, input_size, input_size))
            
            elif measure == 'inference-time':
                # if not 'cuda' in self.device:
                #     raise Exception('Turn on GPU to get inference time')
                
                if args == None:
                    raise Exception('No argparse to get inference time')
                
                model = nasbench1.Network(self.cell, 
                                        stem_out=128, 
                                        num_stacks=3, 
                                        num_mods=3,
                                        num_classes=get_num_classes(args))

                net = model.to(self.device)              
                                        
                starter, ender = torch.cuda.Event(enable_timing=True), torch.cuda.Event(enable_timing=True)

                input = torch.randn(args.batch_size, 3, 32, 32, dtype=torch.float).to(self.device)
                total_time = 0
                num_repetitions = 300

                with torch.no_grad():
                    for rep in range(num_repetitions):
                        starter.record()
                        _ = net(input)
                        ender.record()

                        torch.cuda.synchronize()

                        curr_time = starter.elapsed_time(ender) / 1000
                        total_time += curr_time

                result['inference-time'] = (num_repetitions * args.batch_size) / total_time
                
            # If use zero-cost methods
            else:
                if args == None:
                    raise Exception('No argparse to get Zero-Cost methods')
                if train_loader == None:
                    raise Exception('No train loader')
                
                model = nasbench1.Network(self.cell, 
                                        stem_out=128, 
                                        num_stacks=3, 
                                        num_mods=3,
                                        num_classes=get_num_classes(args))
                
                net = model.to(self.device)
                measures = predictive.find_measures(net, 
                                                train_loader, 
                                                (args.dataload, args.dataload_info, get_num_classes(args)), 
                                                self.device,
                                                measure_names=[measure])   
                result[measure] = measures[measure] if not np.isnan(measures[measure]) else -1e9
            
        
        return result[measure]