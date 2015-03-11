# -*- coding: utf-8 -*-
from atlantis import worker
from atlantis.db import SensorModel, SolutionModel
from atlantis.core.device import AbstractDevice, Sensor
from atlantis.core.problem import Problem
from atlantis.core.solution import Solution
from testutil import DbTestCase, TestCase
import json

class UpdateSensorsTest(DbTestCase):
    def test(self):
        # set up
        class ThermometerDevice(AbstractDevice):
            @Sensor
            def room(self):
                return 25
        class HydrometerDevice(AbstractDevice):
            @Sensor
            def room(self):
                return 50
        
        # test
        with self.mysql.dao.SessionContext():
            worker._update_sensors()
        with self.mysql.dao.create_session() as session:
            sensors = session.query(SensorModel).all()
            self.assertEqual(2, len(sensors))
            self.assertEqual('hydrometer.room', sensors[0].name)
            self.assertEqual(50, json.loads(sensors[0].value))
            self.assertEqual('thermometer.room', sensors[1].name)
            self.assertEqual(25, json.loads(sensors[1].value))
            
class UpdateSolutionStatusesTest(DbTestCase):
    def test(self):
        # set up
        class WindowDevice(AbstractDevice):
            @Solution('thermometer.too_high')
            def open_for_cooling(self):
                pass
            @open_for_cooling.checker
            def check_open(self):
                return True
        class FanDevice(AbstractDevice):
            @Solution('thermometer.too_high')
            def open_for_cooling(self):
                pass
            @open_for_cooling.checker
            def check_open(self):
                return False
        with self.mysql.dao.create_session() as session:
            session.add(SolutionModel(name='window.open_for_cooling', applied=True))
            session.add(SolutionModel(name='fan.open_for_cooling', applied=True))
            
        # test
        with self.mysql.dao.SessionContext():
            worker._update_solution_statuses()
        with self.mysql.dao.create_session() as session:
            self.assertTrue(session.get(SolutionModel, 'window.open_for_cooling').applied)
            self.assertFalse(session.get(SolutionModel, 'fan.open_for_cooling').applied)
            
class CheckProblemsTest(DbTestCase):
    def test_basic(self):
        # set up
        class ThermometerDevice(AbstractDevice):
            @Problem
            def too_high(self):
                return True
        class HumidifierDevice(AbstractDevice):
            @Problem
            def too_high(self):
                return False
            
        # test
        with self.mysql.dao.SessionContext():
            problems = worker._update_problems()
        self.assertEqual(1, len(problems))
        self.assertEqual('thermometer.too_high', problems[0].full_name())
        
    def test_priority(self):
        # set up
        class ThermometerDevice(AbstractDevice):
            @Problem
            def too_high(self):
                return True
        class HumidifierDevice(AbstractDevice):
            @Problem(priority=-1)
            def too_high(self):
                return True
            
        # test
        with self.mysql.dao.SessionContext():
            problems = worker._update_problems()
        self.assertEqual(2, len(problems))
        self.assertEqual('humidifier.too_high', problems[0].full_name())
        self.assertEqual('thermometer.too_high', problems[1].full_name())
        
class FindBestSolutionTest(DbTestCase):
    def test_success(self):
        # set up
        class WindowDevice(AbstractDevice):
            @Solution('thermometer.too_high')
            def open_for_cooling(self):
                pass
            @open_for_cooling.evaluator
            def check_open(self):
                return 100
        class FanDevice(AbstractDevice):
            @Solution('thermometer.too_high')
            def open_for_cooling(self):
                pass
            @open_for_cooling.evaluator
            def check_open(self):
                return 50
            
        # test
        solutions = [WindowDevice().open_for_cooling, FanDevice().open_for_cooling]
        with self.mysql.dao.SessionContext():
            best = worker._find_best_solution(solutions)
        self.assertEqual('window.open_for_cooling', best.full_name())
        
    def test_no_fit(self):
        # set up
        class WindowDevice(AbstractDevice):
            @Solution('thermometer.too_high')
            def open_for_cooling(self):
                pass
            @open_for_cooling.evaluator
            def check_open(self):
                return 0
            
        # test
        solutions = [WindowDevice().open_for_cooling]
        with self.mysql.dao.SessionContext():
            best = worker._find_best_solution(solutions)
        self.assertIsNone(best)
        
class FindSolutionsTest(TestCase):
    def test(self):
        # set up
        class ThermometerDevice(AbstractDevice):
            @Problem
            def too_high(self):
                return True
        class WindowDevice(AbstractDevice):
            @Solution('thermometer.too_high')
            def open_for_cooling(self):
                pass
        class FanDevice(AbstractDevice):
            @Solution('thermometer.too_high')
            def open_for_cooling(self):
                pass
            
        # test
        solutions = worker._find_solutions(ThermometerDevice().too_high)
        self.assertEqual(2, len(solutions))
        self.assertEqual('window.open_for_cooling', solutions[0].full_name())
        self.assertEqual('fan.open_for_cooling', solutions[1].full_name())
        
class ApplySolutionsTest(DbTestCase):
    def test_success(self):
        # set up
        ApplySolutionsTest.solutions = []
        class ThermometerDevice(AbstractDevice):
            @Problem
            def too_high(self):
                return True
        class WindowDevice(AbstractDevice):
            @Solution('thermometer.too_high')
            def open_for_cooling(self):
                ApplySolutionsTest.solutions.append('window.open_for_cooling')
            @open_for_cooling.evaluator
            def evaluate_open_for_cooling(self):
                return 100
        class FanDevice(AbstractDevice):
            @Solution('thermometer.too_high')
            def open_for_cooling(self):
                ApplySolutionsTest.solutions.append('fan.open_for_cooling')
            @open_for_cooling.evaluator
            def evaluate_open_for_cooling(self):
                return 50
        class AirConditioningDevice(AbstractDevice):
            @Solution('thermometer.too_high')
            def open_for_cooling(self):
                ApplySolutionsTest.solutions.append('air_conditioning.open_for_cooling')
            @open_for_cooling.evaluator
            def evaluate_open_for_cooling(self):
                return 0
             
        # test
        with self.mysql.dao.SessionContext():
            problem = ThermometerDevice().too_high
            worker._apply_solutions(problem)
        self.assertEqual(['window.open_for_cooling', 'fan.open_for_cooling'], self.solutions)
        