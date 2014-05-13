# -*- coding: utf-8 -*-
from atlantis import rule
from atlantis.rule import Problem
from fixtures._fixtures.monkeypatch import MonkeyPatch
from fixtures2 import TestCase

class RegisterTest(TestCase):
    def test(self):
        self.useFixture(MonkeyPatch('atlantis.rule.problems', {}))
        class TemperatureTooHighProblem(Problem):
            pass
        class TemperatureTooLowProblem(Problem):
            pass
        self.assertEqual(2, len(rule.problems))
        self.assertIsInstance(rule.problems['TEMPERATURE_TOO_HIGH'], TemperatureTooHighProblem)
        self.assertIsInstance(rule.problems['TEMPERATURE_TOO_LOW'], TemperatureTooLowProblem)
        
class CheckProblemsTest(TestCase):
    def test(self):
        # set up
        self.useFixture(MonkeyPatch('atlantis.rule.problems', {}))
        class TemperatureTooHighProblem(Problem):
            def exists(self):
                return True
        class TemperatureTooLowProblem(Problem):
            def exists(self):
                return False
            
        # test
        problems = rule.check_problems()
        self.assertEqual(1, len(problems))
        self.assertIsInstance(problems[0], TemperatureTooHighProblem)
        