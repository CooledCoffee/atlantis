# -*- coding: utf-8 -*-
from atlantis.db import SolutionModel, ProblemModel
from atlantis.device import AbstractDevice
from atlantis.problem import Problem
from atlantis.solution import Solution, DisableByProblem
from testutil import DbTestCase, TestCase

class SolutionTest(DbTestCase):
    def setUp(self):
        super(SolutionTest, self).setUp()
        class WindowDevice(AbstractDevice):
            @Solution('thermometer.too_high', description='test description')
            def open_for_cooling(self):
                self.opened = True
                
            @Solution('thermometer.too_low', description='test description')
            def open_for_warming(self):
                self.opened = True
                
            @open_for_cooling.checker
            @open_for_warming.checker
            def check_opened(self):
                return True
            
            @open_for_cooling.evaluator
            @open_for_warming.evaluator
            def open_evaluator(self):
                return 50
        self.device = WindowDevice()
        self.solution = self.device.open_for_cooling
            
class InitTest(SolutionTest):
    def test(self):
        self.assertEqual('thermometer.too_high', self.solution.problem)
        self.assertEqual('test description', self.solution.description)
        
class AppliedTest(SolutionTest):
    def test_enabled(self):
        # set up
        with self.mysql.dao.create_session() as session:
            session.add(SolutionModel(name='window.open_for_cooling', applied=True))
            
        # test
        with self.mysql.dao.SessionContext():
            applied = self.solution.applied()
        self.assertTrue(applied)
        
class EnabledTest(SolutionTest):
    def test_enabled(self):
        # set up
        with self.mysql.dao.create_session() as session:
            session.add(SolutionModel(name='window.open_for_cooling', enabled=True))
            
        # test
        with self.mysql.dao.SessionContext():
            enabled = self.solution.enabled()
        self.assertTrue(enabled)
        
class UpdateTest(SolutionTest):
    def test(self):
        # test
        with self.mysql.dao.SessionContext():
            self.solution.update()
        
        # verify
        with self.mysql.dao.create_session() as session:
            self.assertTrue(session.get(SolutionModel, 'window.open_for_cooling').applied)
    
class ApplyTest(SolutionTest):
    def test(self):
        # test
        with self.mysql.dao.SessionContext():
            self.solution.apply()
            
        # verify
        self.assertTrue(self.device.opened)
        with self.mysql.dao.create_session() as session:
            self.assertTrue(session.get(SolutionModel, 'window.open_for_cooling').applied)
        
class CheckerTest(SolutionTest):
    def test_normal(self):
        applied = self.solution._check()
        self.assertTrue(applied)
        
    def test_no_checker(self):
        # set up
        class WindowDevice(AbstractDevice):
            @Solution('thermometer.too_high', description='test description')
            def open_for_cooling(self):
                self.opened = True
        
        # test
        with self.assertRaises(Exception):
            WindowDevice().open_for_cooling._check()

class EvaluateTest(SolutionTest):
    def test_normal(self):
        fitness = self.solution._evaluate()
        self.assertEqual(50, fitness)
        
    def test_no_checker(self):
        # set up
        class WindowDevice(AbstractDevice):
            @Solution('thermometer.too_high', description='test description')
            def open_for_cooling(self):
                self.opened = True
        
        # test
        fitness = WindowDevice().open_for_cooling._evaluate()
        self.assertEqual(100, fitness)
    
class FitnessTest(SolutionTest):
    def test_normal(self):
        with self.mysql.dao.SessionContext():
            fitness = self.solution.fitness()
        self.assertEqual(50, fitness)
        
    def test_already_applied(self):
        # set up
        with self.mysql.dao.create_session() as session:
            session.add(SolutionModel(name='window.open_for_cooling', applied=True))
             
        # test
        with self.mysql.dao.SessionContext():
            fitness = self.solution.fitness()
        self.assertEqual(0, fitness)
        
    def test_disabled(self):
        # set up
        with self.mysql.dao.create_session() as session:
            session.add(SolutionModel(name='window.open_for_cooling', enabled=False))
             
        # test
        with self.mysql.dao.SessionContext():
            fitness = self.solution.fitness()
        self.assertEqual(0, fitness)
        
    def test_error(self):
        # set up
        class WindowDevice(AbstractDevice):
            @Solution('thermometer.too_high', description='test description')
            def open_for_cooling(self):
                pass
            @open_for_cooling.evaluator
            def open_evaluator(self):
                raise Exception()
            
        # test
        with self.mysql.dao.SessionContext():
            fitness = WindowDevice().open_for_cooling.fitness()
        self.assertEqual(0, fitness)
        
class DisableByProblemTest(DbTestCase):
    def setUp(self):
        super(DisableByProblemTest, self).setUp()
        class AtmosphereDevice(AbstractDevice):
            @Problem
            def pollution(self):
                pass
        class WindowDevice(AbstractDevice):
            @Solution('thermometer.too_high')
            def open_for_cooling(self):
                pass
            @open_for_cooling.evaluator
            @DisableByProblem('atmosphere.pollution')
            def open_evaluator(self):
                return 50
        self.solution = WindowDevice().open_for_cooling
        
    def test_exists(self):
        # set up
        with self.mysql.dao.create_session() as session:
            session.add(ProblemModel(name='atmosphere.pollution', exists=True))
            
        # test
        with self.mysql.dao.SessionContext():
            fitness = self.solution.fitness()
        self.assertEqual(0, fitness)
        
    def test_not_exists(self):
        # set up
        with self.mysql.dao.create_session() as session:
            session.add(ProblemModel(name='atmosphere.pollution', exists=False))
            
        # test
        with self.mysql.dao.SessionContext():
            fitness = self.solution.fitness()
        self.assertEqual(50, fitness)
        