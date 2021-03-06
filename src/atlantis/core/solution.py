# -*- coding: utf-8 -*-
from atlantis import core
from atlantis.core.base import DeviceComponent
from atlantis.db import SolutionModel
from decorated import Function
from loggingd import log_enter, log_and_ignore_error
import doctest
import loggingd

log = loggingd.getLogger(__name__)

class Solution(DeviceComponent):
    model_type = SolutionModel
    
    def applied(self, device):
        return self._get_model_field(device, 'applied')
    
    @log_enter('Applying solution {self.full_name(device)} ...')
    def apply(self, device):
        self._call(device)
        model = self._get_model(device, create=True)
        model.applied = True
        
    def checker(self, func):
        self._checker = func
        return func
    
    def enabled(self, device):
        return self._get_model_field(device, 'enabled', default=True)
    
    def evaluator(self, func):
        self._evaluator = func
        return func
    
    def fitness(self, device):
        try:
            if not self.enabled(device):
                return 0
            if self.applied(device):
                return 0
            return self._evaluate(device)
        except:
            log.warn('Failed to calc fitness for "%s".' % self.full_name(device), exc_info=True)
            return 0
        
    @log_enter('[DEBUG] Updating solution status {self.full_name(device)} ...')
    @log_and_ignore_error('Failed to update solution {self.full_name(device)}.', exc_info=True)
    def update(self, device):
        model = self._get_model(device, create=True)
        model.applied = self._check(device)
    
    def _evaluate(self, device):
        if self._evaluator is None:
            return 100
        fitness = self._evaluator(device)
        return _process_fitness(fitness)
    
    def _check(self, device):
        if self._checker is None:
            raise Exception('Solution "%s" does not provide a checker.' % self.full_name(device))
        return self._checker(device)
    
    def _init(self, problem, description=''):
        super(Solution, self)._init()
        self.problem = problem
        self.description = description
        self._checker = None
        self._evaluator = None
        
class DisableByProblem(Function):
    def _call(self, *args, **kw):
        problem = core.clocate(self._problem)
        if problem.exists():
            return 0
        return super(DisableByProblem, self)._call(*args, **kw)
        
    def _init(self, problem):
        super(DisableByProblem, self)._init()
        self._problem = problem
        
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
    