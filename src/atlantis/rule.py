# -*- coding: utf-8 -*-
from atlantis import util
from atlantis.base import AutoRegisterType
from collections import defaultdict

problems = {}
solutions = defaultdict(list)

class Problem(object):
    __metaclass__ = AutoRegisterType
    description = None
    
    @classmethod
    def _register(cls):
        cls.name = util.calc_name(cls).upper()
        problem = cls()
        problems[cls.name] = problem
        
    def exists(self):
        raise NotImplementedError()
    
class Solution(object):
    __metaclass__ = AutoRegisterType
    description = None
    targets = None
    
    @classmethod
    def _register(cls):
        cls.name = util.calc_name(cls).upper()
        solution = cls()
        for target in cls.targets:
            solutions[target.name].append(solution)
    
    def apply(self):
        raise NotImplementedError()
    
    def feasible(self):
        raise NotImplementedError()
    