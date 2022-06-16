from abc import ABC, abstractmethod
import os, sys

class NASBench(ABC):
    _api = None
    @abstractmethod
    def __init__(self):
        self.query_result = None
        self.api = None
        self.op_names = None
        self.cell = None
        self.model_path = None
        self.arch_index = None    

    def convert_individual_to_query(self):
        pass
    
    def query_bench(self, metric=None):
        pass

