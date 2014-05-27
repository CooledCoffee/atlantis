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
        
class UpdateTest(DbTestCase):
    def test(self):
        # set up
        class TemperatureTooHighProblem(Problem):
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
            
class ExistsTest(DbTestCase):
    def test_true(self):
        # set up
        class TemperatureTooHighProblem(Problem):
            pass
        with self.mysql.dao.create_session() as session:
            session.add(ProblemModel(name='TEMPERATURE_TOO_HIGH', exists=True))
            
        # test
        problem = TemperatureTooHighProblem()
        with self.mysql.dao.SessionContext():
            exists = problem.exists()
            self.assertTrue(exists)
            
    def test_false(self):
        # set up
        class TemperatureTooHighProblem(Problem):
            pass
        with self.mysql.dao.create_session() as session:
            session.add(ProblemModel(name='TEMPERATURE_TOO_HIGH', exists=False))
            
        # test
        problem = TemperatureTooHighProblem()
        with self.mysql.dao.SessionContext():
            exists = problem.exists()
            self.assertFalse(exists)
            
    def test_no_record(self):
        # set up
        class TemperatureTooHighProblem(Problem):
            pass
            
        # test
        problem = TemperatureTooHighProblem()
        with self.mysql.dao.SessionContext():
            exists = problem.exists()
            self.assertFalse(exists)
            