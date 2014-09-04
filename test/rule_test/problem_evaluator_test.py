# -*- coding: utf-8 -*-
from atlantis.rule import AbstractProblem, ProblemEvaluator
from fixtures2 import TestCase

class CheckTest(TestCase):
    def test_all_exists(self):
        class Problem1(AbstractProblem):
            def exists(self):
                return True
        class Problem2(AbstractProblem):
            def exists(self):
                return True
        evaluator = ProblemEvaluator(Problem1, Problem2)
        result = evaluator._check()
        self.assertFalse(result)
        
    def test_some_exists(self):
        class Problem1(AbstractProblem):
            def exists(self):
                return True
        class Problem2(AbstractProblem):
            def exists(self):
                return False
        evaluator = ProblemEvaluator(Problem1, Problem2)
        result = evaluator._check()
        self.assertFalse(result)
        
    def test_none_exists(self):
        class Problem1(AbstractProblem):
            def exists(self):
                return False
        class Problem2(AbstractProblem):
            def exists(self):
                return False
        evaluator = ProblemEvaluator(Problem1, Problem2)
        result = evaluator._check()
        self.assertTrue(result)
        