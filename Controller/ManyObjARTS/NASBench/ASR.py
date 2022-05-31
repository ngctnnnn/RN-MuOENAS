import os, sys
from NASBench.NASBench import NASBench 
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from source.NASBenchHW.hw_nas_bench_api import HWNASBenchAPI as HWAPI

class ASR(NASBench):
    def __init__(self):
        super().__init__()
        url = os.path.dirname(__file__)
        self.api = HWAPI(f"{url[:-len('NASBench')] + 'source/NASBenchHW/HW-NAS-Bench-v1_0.pickle'}", search_space="fbnet")
    
    def query_bench(self, ind, dataset, metric=None):
        """
        Arguments:
        dataset -- dataset to query ('cifar100', 'ImageNet')
        metric (optional) -- metric to query ('edgegpu_latency', 
                                            'edgegpu_energy', 
                                            'raspi4_latency', 
                                            'pixel3_latency', 
                                            'eyeriss_latency', 
                                            'eyeriss_energy', 
                                            'fpga_latency', 
                                            'fpga_energy', 
                                            'average_hw_metric')
        """
        if not isinstance(ind, list): # If ind is not list then transform it into list
            ind = ind.tolist()
        self.query_result = self.api.query_by_index(ind, dataset)
        return self.query_result if metric is None else self.query_result[metric] 