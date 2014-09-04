# -*- coding: utf-8 -*-
from atlantis.rule import FixedEvaluator
from fixtures2 import TestCase

class FitnessTest(TestCase):
    def test(self):
        evaluator = FixedEvaluator(50)
        fitness = evaluator.fitness()
        self.assertEqual(50, fitness)
        