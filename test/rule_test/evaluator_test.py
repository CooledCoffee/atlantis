# -*- coding: utf-8 -*-
from atlantis.rule import Evaluator
from fixtures2 import TestCase

class EvaluatorTest(TestCase):
    def test_all_true(self):
        class TestEvaluator(Evaluator):
            def _check_1(self):
                return True
            def _check_2(self):
                return True
        evaluator = TestEvaluator()
        result = evaluator._check()
        self.assertTrue(result)
        
    def test_all_false(self):
        class TestEvaluator(Evaluator):
            def _check_1(self):
                return False
            def _check_2(self):
                return False
        evaluator = TestEvaluator()
        result = evaluator._check()
        self.assertFalse(result)
        
    def test_some_false(self):
        class TestEvaluator(Evaluator):
            def _check_1(self):
                return True
            def _check_2(self):
                return False
        evaluator = TestEvaluator()
        result = evaluator._check()
        self.assertFalse(result)
        
    def test_no_check(self):
        evaluator = Evaluator()
        result = evaluator._check()
        self.assertTrue(result)
        
class FitnessTest(TestCase):
    def test_default(self):
        evaluator = Evaluator()
        fitness = evaluator.fitness()
        self.assertEqual(100, fitness)
        
    def test_number(self):
        class TestEvaluator(Evaluator):
            def _fitness(self):
                return 50
        evaluator = TestEvaluator()
        fitness = evaluator.fitness()
        self.assertEqual(50, fitness)
        
    def test_bool(self):
        class TestEvaluator(Evaluator):
            def _fitness(self):
                return True
        evaluator = TestEvaluator()
        fitness = evaluator.fitness()
        self.assertEqual(100, fitness)
        
    def test_check_failed(self):
        class TestEvaluator(Evaluator):
            def _check_1(self):
                return False
            def _fitness(self):
                return True
        evaluator = TestEvaluator()
        fitness = evaluator.fitness()
        self.assertEqual(0, fitness)
        