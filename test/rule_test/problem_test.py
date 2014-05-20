# -*- coding: utf-8 -*-
from atlantis import rule
from atlantis.db import ProblemModel
from atlantis.rule import Problem
from fixtures._fixtures.monkeypatch import MonkeyPatch
from testutil import DbTestCase, TestCase

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
        
class CheckTest(DbTestCase):
    def test(self):
        # set up
        class TemperatureTooHighProblem(Problem):
            def _exists(self):
                return True
        problem = TemperatureTooHighProblem()
        
        # test
        with self.mysql.dao.SessionContext():
            exists = problem.check()
            
        # verify
        self.assertTrue(exists)
        with self.mysql.dao.create_session() as session:
            model = session.get(ProblemModel, 'TEMPERATURE_TOO_HIGH')
            self.assertTrue(model.exists)
            