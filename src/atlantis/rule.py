# -*- coding: utf-8 -*-
from atlantis import util
from atlantis.base import AutoRegisterType
from atlantis.db import ProblemModel, SolutionModel
from decorated.base.context import ctx
import json

problems = {}
solutions = {}

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
        solutions[cls.name] = solution
    
    def apply(self):
        model = ctx.session.get_or_create(SolutionModel, self.name)
        data = json.loads(model.data) if model.data is not None else None
        data = self._apply(data)
        model.data = json.dumps(data) if data is not None else None
        model.applied = True
        
    def update(self):
        model = ctx.session.get(SolutionModel, self.name)
        model.applied = self._applied()
    
    def _applied(self):
        raise NotImplementedError()
    
    def _apply(self, data):
        raise NotImplementedError()
    
    def _fitness(self):
        raise NotImplementedError()
    