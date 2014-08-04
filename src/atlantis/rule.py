# -*- coding: utf-8 -*-
from atlantis import util
from atlantis.base import AbstractComponent
from atlantis.db import ProblemModel, SolutionModel
from decorated.base.context import ctx
from loggingd import log_enter, log_return, log_and_ignore_error
import doctest
import loggingd

problems = {}
solutions = {}
log = loggingd.getLogger(__name__)

class AbstractProblem(AbstractComponent):
    description = None
    
    @classmethod
    def _register(cls):
        cls.name = util.calc_name(cls).upper()
        problems[cls.name] = cls.instance()
        
    def enabled(self):
        return not _get_bool_field(ProblemModel, self.name, 'disabled', default=False)
        
    def exists(self):
        return _get_bool_field(ProblemModel, self.name, 'exists')
        
    @log_enter('[DEBUG] Updating problem {self.name} ...')
    @log_return('Found problem {self.name}.', condition='ret')
    @log_and_ignore_error('Failed to update problem {self.name}.', exc_info=True)
    def update(self):
        if not self.enabled():
            return False
        exists = self._check()
        model = ctx.session.get_or_create(ProblemModel, self.name)
        model.exists = exists
        return exists
    
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
        
    def enabled(self, problem):
        model = ctx.session.get(SolutionModel, self.name)
        if model is None:
            return True
        return problem.name not in model.disabled.split(',')
        
    def fitness(self, problem):
        try:
            if not self.enabled(problem):
                return 0
            model = ctx.session.get(SolutionModel, self.name)
            if model is not None:
                if model.applied:
                    return 0
            if not self._check_preconditions():
                return 0
            fitness = self._fitness(problem)
            return _process_fitness(fitness)
        except Exception as e:
            log.warn('Failed to calc fitness for "%s".' % self.name)
            return 0
        
    @log_enter('[DEBUG] Updating solution status {self.name} ...')
    @log_and_ignore_error('Failed to update solution {self.name}.', exc_info=True)
    def update(self):
        model = ctx.session.get_or_create(SolutionModel, self.name)
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
    
def _get_bool_field(model_class, key, field, default=False):
    model = ctx.session.get(model_class, key)
    if model is None:
        return default
    return getattr(model, field)

def _process_fitness(fitness):
    '''
    >>> _process_fitness(50)
    50
    >>> _process_fitness(True)
    100
    >>> _process_fitness(False)
    0
    >>> _process_fitness('abc')
    Traceback (most recent call last):
    ...
    Exception: Bad fitness "abc".
    '''
    if fitness is True:
        return 100
    elif fitness is False:
        return 0
    elif isinstance(fitness, (int, float)):
        return fitness
    else:
        raise Exception('Bad fitness "%s".' % fitness)
        
if __name__ == '__main__':
    doctest.testmod()
    