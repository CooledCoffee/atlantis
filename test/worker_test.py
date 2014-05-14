# -*- coding: utf-8 -*-
from atlantis import worker, device
from atlantis.db import SensorModel
from atlantis.device import Device, Sensor
from atlantis.rule import Problem, Solution
from collections import defaultdict
from fixtures._fixtures.monkeypatch import MonkeyPatch
from fixtures2 import TestCase
from testutil import DbTestCase
import json

class UpdateSensorsTest(DbTestCase):
    def test(self):
        # set up
        self.useFixture(MonkeyPatch('atlantis.device.devices', {}))
        class ThermometerDevice(Device):
            temperature = Sensor()
        class HydrometerDevice(Device):
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
        problems = worker._check_problems()
        self.assertEqual(1, len(problems))
        self.assertIsInstance(problems[0], TemperatureTooHighProblem)
        
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
        solutions = worker._find_solutions(problem)
        self.assertEqual(1, len(solutions))
        self.assertIsInstance(solutions[0], OpenWindowSolution)
