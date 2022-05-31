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


def get_num_classes(args):
    if args.dataset == 'cifar100':
        return 100
    if args.dataset == 'cifar10':
        return 10
    if args.dataset == 'imagenet':
        return 120
    raise Exception('Unknown dataset')

class NAS101(NASBench):
    def __init__(self, use_colab=True, debug=False):
        super().__init__()
        
        """ 
        Constants for NASBench101
        """
        INPUT = 'input'
        OUTPUT = 'output'
        CONV3X3 = 'conv3x3-bn-relu'
        CONV1X1 = 'conv1x1-bn-relu'
        MAXPOOL3X3 = 'maxpool3x3'
        NUM_VERTICES = 7
        MAX_EDGES = 9
        EDGE_SPOTS = NUM_VERTICES * (NUM_VERTICES - 1) / 2   # Upper triangular matrix
        OP_SPOTS = NUM_VERTICES - 2   # Input/output vertices are fixed
        ALLOWED_OPS = [CONV3X3, CONV1X1, MAXPOOL3X3]
        ALLOWED_EDGES = [0, 1]   # Binary adjacency matrix
        
        url = os.path.dirname(__file__)
        if debug:
            self.api = None 
        else:
            if not use_colab:
                self.api = api.NASBench(f"{url[:-len('/NASBench')] + '/source/nasbench/nasbench_full.tfrecord'}")
            else:
                self.api = api.NASBench("/content/drive/MyDrive/DTA/Tân/NASBench101/nasbench_full.tfrecord")
        self.cell = None
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        print(f'Running on device: {self.device}')

    def get_individual(self, ind, ops_none=None):
        res = np.zeros((7, 7), dtype=int)
        k = 0
        for i in range(7):
            for j in range(i + 1, 7):
                res[i][j] = ind[k]
                k += 1

        if ops_none != None:
            res = np.delete(res, ops_none, axis=1)
            res = np.delete(res, ops_none, axis=0)
        return res 
   
    def get_operations(self, ind):
        ops_none = []
        ops = ['input']
        for i in range(0, 5):
            if ind[i] == 0:
                ops_none.append(i)
            elif ind[i] == 1:
                ops.append('conv1x1-bn-relu')
            elif ind[i] == 2:
                ops.append('conv3x3-bn-relu')
            else:
                ops.append('maxpool3x3')
        ops.append('output')
        return ops, ops_none

    def get_architecture(self, ind):
        ops, ops_none = self.get_operations(ind)
        ind = self.get_individual(ind[5:], ops_none)
        
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
            self.query_result = self.api.query(self.cell) if 'accuracy' not in metric else self.api.query(self.cell, epochs=epochs)
        except:
            print(f"Cell {self.cell.__dict__['original_matrix']} is invalid for NASBench101")    
            self.api._check_spec(self.cell)

        return self.query_result[metric] if metric is not None else self.query_result 
    
    
    def is_valid(self, ind):
        ops, ops_none = self.get_operations(ind)
        ind = self.convert_ind_triangle(ind[5:], ops_none)
            
        self.cell = api.ModelSpec(ind, ops)
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
        
        ops, ops_none = self.get_operations(ind)
        ind = self.get_individual(ind[5:], ops_none)
        
        self.cell = api.ModelSpec(ind, ops)
        # print(self.cell.__dict__)
         
        if use_csv and not proxy_log:
            raise Exception("No proxy log to query csv")
        
        if 'accuracy' in measure and epoch == None:
            raise Exception('No epoch to evaluate')
        
        proxy_log = {}
        
        result = {}

        # If query from csv file and exists respective log file
        if use_csv and measure in proxy_log:
            pass 

        # If don't use log file, then evaluate directly from NASBench101
        else:
            
            # If measure is 'train_accuracy' or 'validation_accuracy' or 'test_accuracy'
            if epoch != None and 'accuracy' in measure:
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