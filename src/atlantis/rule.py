# -*- coding: utf-8 -*-
from atlantis import util
from atlantis.base import AutoRegisterComponent
from atlantis.db import ProblemModel, SolutionModel
from decorated.base.context import ctx
from loggingd import log_enter, log_return

problems = {}
solutions = {}

class Problem(AutoRegisterComponent):
    description = None
    
    @classmethod
    def _register(cls):
        cls.name = util.calc_name(cls).upper()
        problems[cls.name] = cls.instance()
        
    @log_enter('[DEBUG] Updating problem {self.name} ...')
    @log_return('Found problem {self.name}.', condition='ret')
    def update(self):
        model = ctx.session.get_or_create(ProblemModel, self.name)
        if model.exists is None:
            model.exists = False
        model.exists = self._check()
        return model.exists
    
    def exists(self):
        return _get_bool_field(ProblemModel, self.name, 'exists')
        
    def _check(self):
        raise NotImplementedError()
    
class Solution(AutoRegisterComponent):
    description = None
    preconditions = []
    targets = []
    
    @classmethod
    def _register(cls):
        cls.name = util.calc_name(cls).upper()
        solutions[cls.name] = cls.instance()
        
    def applied(self):
        return _get_bool_field(ProblemModel, self.name, 'applied')
    
    @log_enter('Applying solution {self.name} ...')
    def apply(self, problem):
        self._apply(problem)
        model = ctx.session.get_or_create(SolutionModel, self.name)
        model.applied = True
        
    def fitness(self, problem):
        model = ctx.session.get(SolutionModel, self.name)
        if model is not None and model.applied:
            return 0
        if not self._check_preconditions():
            return 0
        fitness = self._fitness(problem)
        if fitness is True:
            fitness = 100
        elif fitness is False:
            fitness = 0
        return fitness
        
    @log_enter('[DEBUG] Updating solution status {self.name} ...')
    def update(self):
        model = ctx.session.get(SolutionModel, self.name)
        model.applied = self._check()
    
    def _apply(self, problem, data):
        raise NotImplementedError()
    
    def _check(self):
        raise NotImplementedError()
    
    def _check_preconditions(self):
        for problem in self.preconditions:
            problem = problems[problem.name]
            if problem.exists():
                return False
        return True
    
    def _fitness(self, problem):
        return True
    
def _get_bool_field(model_class, key, field):
    model = ctx.session.get(model_class, key)
    if model is None:
        return False
    return getattr(model, field)
