# from ZeroCostNas.foresight.dataset import get_cifar_dataloaders
# import argparse

# dataset = 'cifar10'
# train_loader, test_loader = get_cifar_dataloaders(64, 64, dataset, 2)
# dataset_args = 'imagenet' if dataset == 'ImageNet16-120' else dataset

# args = argparse.Namespace(api_loc='', 
#                           outdir='',
#                           init_w_type='none', # Initialize weight
#                           init_b_type='none', # Initialize bias
#                           batch_size=64,      # Batch size
#                           dataset=dataset_args,
#                           gpu=0,
#                           num_data_workers=2,
#                           dataload='random',
#                           dataload_info=1,
#                           seed=1,
#                           write_freq=1,
#                           start=0,
#                           end=0,
#                           noacc=False
#                           )

# """
# NATS-Bench
# """
# from numpy import genfromtxt
# from NASBench import NATS

# api = NATS.NATS(use_colab=False)
# api.evaluate_arch(args=args, ind=[2, 3, 1, 0, 4, 2], dataset=dataset, measure='synflow', train_loader=train_loader)


# """
# NAS-Bench-101
# """

# # from NASBench import NAS101
# # from ZeroCostNas.foresight.dataset import get_cifar_dataloaders
# # import numpy as np
# # import argparse

# # api = NAS101.NAS101(use_colab=False)
# # print(api.evaluate_arch(args, ind=[2, 3, 0, 2, 2, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1,
# #         0, 1, 1, 0], measure='macs', train_loader=train_loader))


from algorithm.utils.custom_operations import TwoPointsCrossover
from algorithm.utils.factory import get_crossover, get_sampling
import numpy as np
from search101 import NASBench101
from algorithm.pymoo.pymoo.interface import crossover
import NASBench

pop = np.array([[4, 2, 3, 2, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0,
        0, 0, 0, 1],
       [0, 1, 4, 4, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0,
        0, 1, 1, 1]])
pop2 = np.array([  
       [1, 1, 1, 2, 3, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0,
        1, 1, 0, 0],
       [4, 4, 0, 4, 3, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1,
        0, 1, 0, 0]])

# crossover_operation = get_crossover('int_one_point', prob=0.9)
# pop_size = 20
# pareto_front_url = 'a.txt'
# generations = 50
# n_obj = 2
# problem = NASBench101(n_var=6, 
#                     n_obj=n_obj, 
#                     xl=0, 
#                     xu=4, 
#                     api=NASBench.NAS101.NAS101(use_colab=False, debug=True), 
#                     dataset='cifar10',
#                     pareto_front_url=pareto_front_url,
#                     proxy_log = {
#                         'flops': 'a.txt'
#                     })

# sample = get_sampling("int_random")
def example_parents(n_matings, n_var):
    a = np.arange(n_var)[None, :].repeat(n_matings, axis=0)
    b = a + n_var
    return a, b


n_matings, n_var = 1, 10
a,b = example_parents(n_matings,n_var)
print(a)
print(b)
off = crossover(get_crossover('int_ux'), a, b)
print(off)