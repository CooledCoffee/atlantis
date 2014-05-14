# -*- coding: utf-8 -*-
from atlantis import util
from atlantis.base import AutoRegisterType
from atlantis.db import ProblemModel, SolutionModel
from collections import defaultdict
from datetime import datetime
from decorated.base.context import ctx
import json

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
        
    def check(self):
        model = ctx.session.get_or_create(ProblemModel, self.name)
        model.exists = self._exists()
        return model.exists
        
    def _exists(self):
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
        model = ctx.session.get_or_create(SolutionModel, self.name)
        data = json.loads(model.data) if model.data is not None else None
        data = self._apply(data)
        model.data = json.dumps(data) if data is not None else None
        model.applied = True
    
    def _apply(self, data):
        raise NotImplementedError()
    
    def _fitness(self):
        raise NotImplementedError()
    