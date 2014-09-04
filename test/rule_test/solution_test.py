# -*- coding: utf-8 -*-
from atlantis import rule
from atlantis.db import SolutionModel
from atlantis.rule import AbstractSolution, AbstractProblem, Evaluator
from fixtures._fixtures.monkeypatch import MonkeyPatch
from testutil import DbTestCase, TestCase

class RegisterTest(TestCase):
    def test(self):
        self.useFixture(MonkeyPatch('atlantis.rule.solutions', {}))
        class OpenWindowSolution(AbstractSolution):
            targets = []
        class OpenAirConditioningSolution(AbstractSolution):
            targets = []
        self.assertEqual(2, len(rule.solutions))
        self.assertIsInstance(rule.solutions['OPEN_WINDOW'], OpenWindowSolution)
        self.assertIsInstance(rule.solutions['OPEN_AIR_CONDITIONING'], OpenAirConditioningSolution)
        
class EnabledTest(DbTestCase):
    def setUp(self):
        super(EnabledTest, self).setUp()
        class TemperatureTooHighProblem(AbstractProblem):
            pass
        class OpenWindowSolution(AbstractSolution):
            pass
        self.problem = TemperatureTooHighProblem()
        self.solution = OpenWindowSolution()
        
    def test_enabled(self):
        with self.mysql.dao.create_session() as session:
            session.add(SolutionModel(name='OPEN_WINDOW', disabled='BAD_ATMOSPHERE'))
        with self.mysql.dao.SessionContext():
            result = self.solution.enabled(self.problem)
        self.assertTrue(result)
        
    def test_disabled(self):
        with self.mysql.dao.create_session() as session:
            session.add(SolutionModel(name='OPEN_WINDOW', disabled='TEMPERATURE_TOO_HIGH,TEMPERATURE_TOO_LOW'))
        with self.mysql.dao.SessionContext():
            result = self.solution.enabled(self.problem)
        self.assertFalse(result)
        
    def test_no_disable(self):
        with self.mysql.dao.create_session() as session:
            session.add(SolutionModel(name='OPEN_WINDOW', disabled=''))
        with self.mysql.dao.SessionContext():
            result = self.solution.enabled(self.problem)
        self.assertTrue(result)
        
    def test_no_model(self):
        with self.mysql.dao.SessionContext():
            result = self.solution.enabled(self.problem)
        self.assertTrue(result)
            
class ApplyTest(DbTestCase):
    def test(self):
        # set up
        class OpenWindowSolution(AbstractSolution):
            targets = []
            def _apply(self, problem):
                ApplyTest.problem = problem
        
        # test
        problem = object()
        solution = OpenWindowSolution()
        with self.mysql.dao.SessionContext():
            solution.apply(problem)
        self.assertEqual(problem, self.problem)
        with self.mysql.dao.create_session() as session:
            model = session.get(SolutionModel, 'OPEN_WINDOW')
            self.assertTrue(model.applied)

class UpdateTest(DbTestCase):
    def test(self):
        # set up
        class OpenWindowSolution(AbstractSolution):
            targets = []
            def _check(self):
                return False
        with self.mysql.dao.create_session() as session:
            session.add(SolutionModel(name='OPEN_WINDOW', applied=True))
            
        # test
        solution = OpenWindowSolution()
        with self.mysql.dao.SessionContext():
            solution.update()
        with self.mysql.dao.create_session() as session:
            model = session.get(SolutionModel, 'OPEN_WINDOW')
            self.assertFalse(model.applied)
            
class FitnessTest(DbTestCase):
    def setUp(self):
        super(FitnessTest, self).setUp()
        class TemperatureTooHighProblem(AbstractProblem):
            pass
        self.Problem = TemperatureTooHighProblem
        self.problem = TemperatureTooHighProblem()
        
    def test_normal(self):
        # set up
        class TestEvaluator(Evaluator):
            def _fitness(self):
                return 50
        class OpenWindowSolution(AbstractSolution):
            targets = {
                self.Problem: TestEvaluator(),
            }
            
        # test
        solution = OpenWindowSolution()
        with self.mysql.dao.SessionContext():
            fitness = solution.fitness(self.problem)
        self.assertEqual(50, fitness)
        
    def test_default(self):
        # set up
        class OpenWindowSolution(AbstractSolution):
            targets = {
                self.Problem: None,
            }
            
        # test
        solution = OpenWindowSolution()
        with self.mysql.dao.SessionContext():
            fitness = solution.fitness(self.problem)
        self.assertEqual(100, fitness)
        
    def test_already_applied(self):
        # set up
        class OpenWindowSolution(AbstractSolution):
            targets = {
                self.Problem: None,
            }
        with self.mysql.dao.create_session() as session:
            session.add(SolutionModel(name='OPEN_WINDOW', applied=True))
            
        # test
        solution = OpenWindowSolution()
        with self.mysql.dao.SessionContext():
            fitness = solution.fitness(self.problem)
        self.assertEqual(0, fitness)
        
    def test_disabled(self):
        # set up
        class OpenWindowSolution(AbstractSolution):
            targets = {
                self.Problem: None,
            }
        with self.mysql.dao.create_session() as session:
            session.add(SolutionModel(name='OPEN_WINDOW', applied=False, disabled='TEMPERATURE_TOO_HIGH,TEMPERATURE_TOO_LOW'))
            
        # test
        solution = OpenWindowSolution()
        with self.mysql.dao.SessionContext():
            fitness = solution.fitness(self.problem)
        self.assertEqual(0, fitness)
        
    def test_error(self):
        # set up
        class TestEvaluator(Evaluator):
            def _fitness(self):
                raise Exception()
        class OpenWindowSolution(AbstractSolution):
            targets = {
                self.Problem: TestEvaluator(),
            }
            
        # test
        solution = OpenWindowSolution()
        with self.mysql.dao.SessionContext():
            fitness = solution.fitness(self.problem)
        self.assertEqual(0, fitness)
        