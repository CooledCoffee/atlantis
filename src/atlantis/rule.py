# -*- coding: utf-8 -*-
from atlantis import util
from atlantis.base import AbstractComponent
from atlantis.db import ProblemModel, SolutionModel
from decorated.base.context import ctx
from loggingd import log_enter, log_return, log_and_ignore_error

problems = {}
solutions = {}

class AbstractProblem(AbstractComponent):
    description = None
    
    @classmethod
    def _register(cls):
        cls.name = util.calc_name(cls).upper()
        problems[cls.name] = cls.instance()
        
    @log_enter('[DEBUG] Updating problem {self.name} ...')
    @log_return('Found problem {self.name}.', condition='ret')
    @log_and_ignore_error('Failed to update problem {self.name}.', exc_info=True)
    def update(self):
        exists = self._check()
        model = ctx.session.get_or_create(ProblemModel, self.name)
        model.exists = exists
        return exists
    
    def exists(self):
        return _get_bool_field(ProblemModel, self.name, 'exists')
        
    def _check(self):
        raise NotImplementedError()
    
class AbstractSolution(AbstractComponent):
    description = None
    preconditions = []
    targets = None
    
    @classmethod
    def _register(cls):
        cls.name = util.calc_name(cls).upper()
        solutions[cls.name] = cls.instance()
        
    def applied(self):
        return _get_bool_field(SolutionModel, self.name, 'applied')
    
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
    @log_and_ignore_error('Failed to update problem {self.name}.', exc_info=True)
    def update(self):
        model = ctx.session.get(SolutionModel, self.name)
        model.applied = self._check()
    
    def _apply(self, problem):
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
