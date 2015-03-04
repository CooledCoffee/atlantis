# -*- coding: utf-8 -*-
from atlantis import util
from atlantis.base import AbstractComponent
from atlantis.db import SolutionModel
from decorated.base.context import ctx
from loggingd import log_enter, log_and_ignore_error
import doctest
import loggingd

problems = {}
solutions = {}
log = loggingd.getLogger(__name__)

class Evaluator(object):
    def fitness(self):
        if not self._check():
            return 0
        fitness = self._fitness()
        return _process_fitness(fitness)
    
    def _check(self):
        for attr in dir(self):
            if not attr.startswith('_check_'):
                continue
            attr = getattr(self, attr)
            if not callable(attr):
                continue
            if not attr():
                return False
        return True
    
    def _fitness(self):
        return True
    
class FixedEvaluator(Evaluator):
    def __init__(self, fitness):
        super(FixedEvaluator, self).__init__()
        self._value = fitness
        
    def _fitness(self):
        return self._value
    
class ProblemEvaluator(Evaluator):
    def __init__(self, *classes):
        super(ProblemEvaluator, self).__init__()
        self._classes = classes
        
    def _check_problems(self):
        for cls in self._classes:
            if cls.instance().exists():
                return False
        return True

if __name__ == '__main__':
    doctest.testmod()
    