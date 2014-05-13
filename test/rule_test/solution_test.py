# -*- coding: utf-8 -*-
from atlantis import rule
from atlantis.rule import Problem, Solution
from collections import defaultdict
from fixtures._fixtures.monkeypatch import MonkeyPatch
from fixtures2 import TestCase

class RegisterTest(TestCase):
    def test(self):
        self.useFixture(MonkeyPatch('atlantis.rule.solutions', defaultdict(list)))
        class TemperatureTooHighProblem(Problem):
            pass
        class TemperatureTooLowProblem(Problem):
            pass
        class OpenWindowSolution(Solution):
            targets = [TemperatureTooHighProblem, TemperatureTooLowProblem]
        class OpenAirConditioningSolution(Solution):
            targets = [TemperatureTooHighProblem]
        self.assertEqual(2, len(rule.solutions))
        self.assertEqual([OpenWindowSolution, OpenAirConditioningSolution], rule.solutions[TemperatureTooHighProblem])
        self.assertEqual([OpenWindowSolution], rule.solutions[TemperatureTooLowProblem])
            
class FindSolutionsTest(TestCase):
    def test(self):
        # set up
        self.useFixture(MonkeyPatch('atlantis.rule.solutions', defaultdict(list)))
        class TemperatureTooHighProblem(Problem):
            pass
        class OpenWindowSolution(Solution):
            targets = [TemperatureTooHighProblem]
            def feasible(self):
                return True
        class OpenAirConditioningSolution(Solution):
            targets = [TemperatureTooHighProblem]
            def feasible(self):
                return False
    
        # test
        problem = TemperatureTooHighProblem()
        solutions = rule.find_solutions(problem)
        self.assertEqual(1, len(solutions))
        self.assertIsInstance(solutions[0], OpenWindowSolution)
