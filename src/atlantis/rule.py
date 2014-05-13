# -*- coding: utf-8 -*-
from atlantis.base import AutoRegisterType
from collections import defaultdict

problems = []
solutions = defaultdict(list)

class Problem(object):
    __metaclass__ = AutoRegisterType
    description = None
    
    @classmethod
    def _register(cls):
        problems.append(cls)
        
    def exists(self):
        raise NotImplementedError()
    
class Solution(object):
    __metaclass__ = AutoRegisterType
    description = None
    targets = None
    
    @classmethod
    def _register(cls):
        for target in cls.targets:
            solutions[target].append(cls)
    
    def apply(self):
        raise NotImplementedError()
    
    def feasible(self):
        raise NotImplementedError()
    
def check_problems():
    instances = [p() for p in problems]
    return [p for p in instances if p.exists()]
    
def find_solutions(problem):
    candidates = solutions[type(problem)]
    candidates = [c() for c in candidates]
    candidates = [c for c in candidates if c.feasible()]
    return candidates
