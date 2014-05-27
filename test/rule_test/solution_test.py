# -*- coding: utf-8 -*-
from atlantis import rule
from atlantis.db import SolutionModel
from atlantis.rule import Solution, Problem
from fixtures._fixtures.monkeypatch import MonkeyPatch
from testutil import DbTestCase, TestCase
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
        case = self
        p = object()
        class OpenWindowSolution(Solution):
            targets = []
            def _apply(self, problem, data):
                case.assertEqual(p, problem)
        
        # test
        solution = OpenWindowSolution()
        with self.mysql.dao.SessionContext():
            solution.apply(p)
        with self.mysql.dao.create_session() as session:
            model = session.get(SolutionModel, 'OPEN_WINDOW')
            self.assertTrue(model.applied)
            
    def test_data(self):
        # set up
        case = self
        class OpenWindowSolution(Solution):
            targets = []
            def _apply(self, problem, data):
                case.assertEqual('old data', data)
                return 'new data'
        with self.mysql.dao.create_session() as session:
            session.add(SolutionModel(name='OPEN_WINDOW', applied=True, data=json.dumps('old data')))
        
        # test
        solution = OpenWindowSolution()
        with self.mysql.dao.SessionContext():
            solution.apply(None)
        with self.mysql.dao.create_session() as session:
            model = session.get(SolutionModel, 'OPEN_WINDOW')
            self.assertTrue(model.applied)
            self.assertEqual('new data', json.loads(model.data))

class UpdateTest(DbTestCase):
    def test(self):
        # set up
        class OpenWindowSolution(Solution):
            targets = []
            def _check(self):
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
            
class FitnessTest(DbTestCase):
    def test_default(self):
        # set up
        class OpenWindowSolution(Solution):
            targets = []
            
        # test
        solution = OpenWindowSolution()
        with self.mysql.dao.SessionContext():
            fitness = solution.fitness(None)
        self.assertEqual(100, fitness)
        
    def test_number(self):
        # set up
        class OpenWindowSolution(Solution):
            targets = []
            def _fitness(self, problem):
                return 100
            
        # test
        solution = OpenWindowSolution()
        with self.mysql.dao.SessionContext():
            fitness = solution.fitness(None)
        self.assertEqual(100, fitness)
        
    def test_true(self):
        # set up
        class OpenWindowSolution(Solution):
            targets = []
            def _fitness(self, problem):
                return True
        with self.mysql.dao.create_session() as session:
            session.add(SolutionModel(name='OPEN_WINDOW', applied=False))
            
        # test
        solution = OpenWindowSolution()
        with self.mysql.dao.SessionContext():
            fitness = solution.fitness(None)
        self.assertEqual(100, fitness)
        
    def test_false(self):
        # set up
        class OpenWindowSolution(Solution):
            targets = []
            def _fitness(self, problem):
                return False
        with self.mysql.dao.create_session() as session:
            session.add(SolutionModel(name='OPEN_WINDOW', applied=False))
            
        # test
        solution = OpenWindowSolution()
        with self.mysql.dao.SessionContext():
            fitness = solution.fitness(None)
        self.assertIs(fitness, 0)
        
    def test_not_fit(self):
        # set up
        class OpenWindowSolution(Solution):
            targets = []
            def _fitness(self, problem):
                return 0
        with self.mysql.dao.create_session() as session:
            session.add(SolutionModel(name='OPEN_WINDOW', applied=False))
            
        # test
        solution = OpenWindowSolution()
        with self.mysql.dao.SessionContext():
            fitness = solution.fitness(None)
        self.assertEqual(0, fitness)
        
    def test_already_applied(self):
        # set up
        class OpenWindowSolution(Solution):
            targets = []
            def _fitness(self, problem):
                return 100
        with self.mysql.dao.create_session() as session:
            session.add(SolutionModel(name='OPEN_WINDOW', applied=True))
            
        # test
        solution = OpenWindowSolution()
        with self.mysql.dao.SessionContext():
            fitness = solution.fitness(None)
        self.assertEqual(0, fitness)
        
    def test_pre_conditions_fail(self):
        # set up
        class BadAtmosphereProblem(Problem):
            def exists(self):
                return True
        class OpenWindowSolution(Solution):
            preconditions = [BadAtmosphereProblem]
            targets = []
            def _fitness(self, problem):
                return 100
            
        # test
        solution = OpenWindowSolution()
        with self.mysql.dao.SessionContext():
            fitness = solution.fitness(None)
        self.assertEqual(0, fitness)
        