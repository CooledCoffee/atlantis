# -*- coding: utf-8 -*-
from atlantis import rule
from atlantis.db import SolutionModel
from atlantis.rule import Solution
from fixtures._fixtures.monkeypatch import MonkeyPatch
from fixtures2 import TestCase
from testutil import DbTestCase
import json

class RegisterTest(TestCase):
    def test(self):
        self.useFixture(MonkeyPatch('atlantis.rule.solutions', {}))
        class OpenWindowSolution(Solution):
            targets = []
        class OpenAirConditioningSolution(Solution):
            targets = []
        self.assertEqual(2, len(rule.solutions))
        self.assertIsInstance(rule.solutions['OPEN_WINDOW'], OpenWindowSolution)
        self.assertIsInstance(rule.solutions['OPEN_AIR_CONDITIONING'], OpenAirConditioningSolution)
        
class ApplyTest(DbTestCase):
    def test_simple(self):
        # set up
        class OpenWindowSolution(Solution):
            targets = []
            def _apply(self, data):
                pass
        
        # test
        solution = OpenWindowSolution()
        with self.mysql.dao.SessionContext():
            solution.apply()
        with self.mysql.dao.create_session() as session:
            model = session.get(SolutionModel, 'OPEN_WINDOW')
            self.assertTrue(model.applied)
            
    def test_data(self):
        # set up
        case = self
        class OpenWindowSolution(Solution):
            targets = []
            def _apply(self, data):
                case.assertEqual('old data', data)
                return 'new data'
        with self.mysql.dao.create_session() as session:
            session.add(SolutionModel(name='OPEN_WINDOW', applied=True, data=json.dumps('old data')))
        
        # test
        solution = OpenWindowSolution()
        with self.mysql.dao.SessionContext():
            solution.apply()
        with self.mysql.dao.create_session() as session:
            model = session.get(SolutionModel, 'OPEN_WINDOW')
            self.assertTrue(model.applied)
            self.assertEqual('new data', json.loads(model.data))

class UpdateTest(DbTestCase):
    def test(self):
        # set up
        class OpenWindowSolution(Solution):
            targets = []
            def _applied(self):
                return False
        with self.mysql.dao.create_session() as session:
            session.add(SolutionModel(name='OPEN_WINDOW', applied=True, data=json.dumps('old data')))
            
        # test
        solution = OpenWindowSolution()
        with self.mysql.dao.SessionContext():
            solution.update()
        with self.mysql.dao.create_session() as session:
            model = session.get(SolutionModel, 'OPEN_WINDOW')
            self.assertFalse(model.applied)
            
class CheckTest(DbTestCase):
    def test_ok_1(self):
        # set up
        class OpenWindowSolution(Solution):
            targets = []
            def _fitness(self):
                return 100
        with self.mysql.dao.create_session() as session:
            session.add(SolutionModel(name='OPEN_WINDOW', applied=False))
            
        # test
        solution = OpenWindowSolution()
        with self.mysql.dao.SessionContext():
            fitness = solution.check()
        self.assertEqual(100, fitness)
        
    def test_ok_2(self):
        # set up
        class OpenWindowSolution(Solution):
            targets = []
            def _fitness(self):
                return 100
            
        # test
        solution = OpenWindowSolution()
        with self.mysql.dao.SessionContext():
            fitness = solution.check()
        self.assertEqual(100, fitness)
        
    def test_not_fit(self):
        # set up
        class OpenWindowSolution(Solution):
            targets = []
            def _fitness(self):
                return 0
        with self.mysql.dao.create_session() as session:
            session.add(SolutionModel(name='OPEN_WINDOW', applied=False))
            
        # test
        solution = OpenWindowSolution()
        with self.mysql.dao.SessionContext():
            fitness = solution.check()
        self.assertEqual(0, fitness)
        
    def test_already_applied(self):
        # set up
        class OpenWindowSolution(Solution):
            targets = []
            def _fitness(self):
                return 100
        with self.mysql.dao.create_session() as session:
            session.add(SolutionModel(name='OPEN_WINDOW', applied=True))
            
        # test
        solution = OpenWindowSolution()
        with self.mysql.dao.SessionContext():
            fitness = solution.check()
        self.assertEqual(0, fitness)
        