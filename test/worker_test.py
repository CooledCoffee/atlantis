# -*- coding: utf-8 -*-
from atlantis import worker, device
from atlantis.db import SensorModel, SolutionModel
from atlantis.device import AbstractDevice, Sensor
from atlantis.rule import AbstractProblem, AbstractSolution
from fixtures._fixtures.monkeypatch import MonkeyPatch
from testutil import DbTestCase, TestCase
import json

class UpdateSensorsTest(DbTestCase):
    def test(self):
        # set up
        self.useFixture(MonkeyPatch('atlantis.device.devices', {}))
        class ThermometerDevice(AbstractDevice):
            temperature = Sensor()
        class HydrometerDevice(AbstractDevice):
            humidity = Sensor()
        device.devices['thermometer'].temperature._retrieve = lambda: 25
        device.devices['hydrometer'].humidity._retrieve = lambda: 50
        
        # test
        with self.mysql.dao.SessionContext():
            worker._update_sensors()
        with self.mysql.dao.create_session() as session:
            sensors = session.query(SensorModel).all()
            self.assertEqual(2, len(sensors))
            self.assertEqual('hydrometer.humidity', sensors[0].name)
            self.assertEqual(50, json.loads(sensors[0].value))
            self.assertEqual('thermometer.temperature', sensors[1].name)
            self.assertEqual(25, json.loads(sensors[1].value))
            
class UpdateSolutionStatusesTest(DbTestCase):
    def test(self):
        # set up
        class OpenWindowSolution(AbstractSolution):
            targets = []
            def _check(self):
                return True
        class OpenAirConditioningSolution(AbstractSolution):
            targets = []
            def _check(self):
                return False
        with self.mysql.dao.create_session() as session:
            session.add(SolutionModel(name='OPEN_WINDOW', applied=True))
            session.add(SolutionModel(name='OPEN_AIR_CONDITIONING', applied=True))
            session.add(SolutionModel(name='OPEN_FAN', applied=False))
            
        # test
        with self.mysql.dao.SessionContext():
            worker._update_solution_statuses()
        with self.mysql.dao.create_session() as session:
            self.assertTrue(session.get(SolutionModel, 'OPEN_WINDOW').applied)
            self.assertFalse(session.get(SolutionModel, 'OPEN_AIR_CONDITIONING').applied)
            self.assertFalse(session.get(SolutionModel, 'OPEN_FAN').applied)
            
class CheckProblemsTest(TestCase):
    def test(self):
        # set up
        self.useFixture(MonkeyPatch('atlantis.rule.problems', {}))
        class TemperatureTooHighProblem(AbstractProblem):
            def update(self):
                return True
        class TemperatureTooLowProblem(AbstractProblem):
            def update(self):
                return False
            
        # test
        problems = worker._update_problems()
        self.assertEqual(1, len(problems))
        self.assertIsInstance(problems[0], TemperatureTooHighProblem)
        
class FindBestSolutionTest(TestCase):
    def test_success(self):
        # set up
        self.useFixture(MonkeyPatch('atlantis.rule.solutions', {}))
        class TemperatureTooHighProblem(AbstractProblem):
            pass
        class OpenWindowSolution(AbstractSolution):
            targets = [TemperatureTooHighProblem]
            def fitness(self, problem):
                return 100
        class OpenAirConditioningSolution(AbstractSolution):
            targets = [TemperatureTooHighProblem]
            def fitness(self, problem):
                return 0
            
        # test
        problem = TemperatureTooHighProblem()
        solution = worker._find_best_solution(problem)
        self.assertIsInstance(solution, OpenWindowSolution)
        
    def test_no_solution(self):
        # set up
        self.useFixture(MonkeyPatch('atlantis.rule.solutions', {}))
        class TemperatureTooHighProblem(AbstractProblem):
            pass
        class OpenWindowSolution(AbstractSolution):
            targets = [TemperatureTooHighProblem]
            def fitness(self, problem):
                return 0
            
        # test
        problem = TemperatureTooHighProblem()
        solution = worker._find_best_solution(problem)
        self.assertIsNone(solution)
        