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
        self.assertIsInstance(rule.solutions['TEMPERATURE_TOO_HIGH'][0], OpenWindowSolution)
        self.assertIsInstance(rule.solutions['TEMPERATURE_TOO_HIGH'][1], OpenAirConditioningSolution)
        self.assertIsInstance(rule.solutions['TEMPERATURE_TOO_LOW'][0], OpenWindowSolution)
        