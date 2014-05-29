# -*- coding: utf-8 -*-
from atlantis import rule
from atlantis.db import ProblemModel
from atlantis.rule import AbstractProblem
from fixtures._fixtures.monkeypatch import MonkeyPatch
from testutil import DbTestCase, TestCase

class RegisterTest(TestCase):
    def test(self):
        self.useFixture(MonkeyPatch('atlantis.rule.problems', {}))
        class TemperatureTooHighProblem(AbstractProblem):
            pass
        class TemperatureTooLowProblem(AbstractProblem):
            pass
        self.assertEqual(2, len(rule.problems))
        self.assertIsInstance(rule.problems['TEMPERATURE_TOO_HIGH'], TemperatureTooHighProblem)
        self.assertIsInstance(rule.problems['TEMPERATURE_TOO_LOW'], TemperatureTooLowProblem)
        
class UpdateTest(DbTestCase):
    def test(self):
        # set up
        class TemperatureTooHighProblem(AbstractProblem):
            def _check(self):
                return True
        problem = TemperatureTooHighProblem()
        
        # test
        with self.mysql.dao.SessionContext():
            exists = problem.update()
            
        # verify
        self.assertTrue(exists)
        with self.mysql.dao.create_session() as session:
            model = session.get(ProblemModel, 'TEMPERATURE_TOO_HIGH')
            self.assertTrue(model.exists)
            