# -*- coding: utf-8 -*-
from atlantis import util
from atlantis.base import AutoRegisterType
from atlantis.db import ProblemModel, SolutionModel
from decorated.base.context import ctx
from loggingd import log_enter, log_return
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
        
    @log_enter('[DEBUG] Checking problem {self.name} ...')
    @log_return('Found problem {self.name}.', condition='ret')
    def check(self):
        model = ctx.session.get_or_create(ProblemModel, self.name)
        model.exists = self._exists()
        return model.exists
    
    def exists(self):
        model = ctx.session.get(ProblemModel, self.name)
        if model is None:
            return False
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
    
    @log_enter('Applying solution {self.name} ...')
    def apply(self, problem):
        model = ctx.session.get_or_create(SolutionModel, self.name)
        data = json.loads(model.data) if model.data is not None else None
        data = self._apply(problem, data)
        model.data = json.dumps(data) if data is not None else None
        model.applied = True
        
    def check(self, problem):
        model = ctx.session.get(SolutionModel, self.name)
        if model is not None and model.applied:
            return 0
        if not self._precondition():
            return 0
        return self._fitness(problem)
        
    @log_enter('[DEBUG] Updating solution status {self.name} ...')
    def update(self):
        model = ctx.session.get(SolutionModel, self.name)
        model.applied = self._applied()
    
    def _applied(self):
        raise NotImplementedError()
    
    def _apply(self, problem, data):
        raise NotImplementedError()
    
    def _fitness(self, problem):
        raise NotImplementedError()
    
    def _precondition(self):
        return True
    