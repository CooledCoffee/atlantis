# -*- coding: utf-8 -*-
from atlantis.db import ProblemModel
from atlantis.device import AbstractDevice, Problem
from testutil import DbTestCase

class ProblemTest(DbTestCase):
    def setUp(self):
        super(ProblemTest, self).setUp()
        class ThermometerDevice(AbstractDevice):
            @Problem(priority=1, description='test description')
            def too_high(self):
                return True
        self.problem = ThermometerDevice().too_high
        
class InitTest(ProblemTest):
    def test(self):
        self.assertEqual('test description', self.problem.description)
        self.assertEqual(1, self.problem.priority)
        
class EnabledTest(ProblemTest):
    def test_enabled(self):
        # set up
        with self.mysql.dao.create_session() as session:
            session.add(ProblemModel(name='thermometer.too_high', disabled=False))
            
        # test
        with self.mysql.dao.SessionContext():
            enabled = self.problem.enabled()
        self.assertTrue(enabled)
        
class ExistsTest(ProblemTest):
    def test_enabled(self):
        # set up
        with self.mysql.dao.create_session() as session:
            session.add(ProblemModel(name='thermometer.too_high', exists=True))
            
        # test
        with self.mysql.dao.SessionContext():
            exists = self.problem.exists()
        self.assertTrue(exists)
        
class UpdateTest(ProblemTest):
    def test_normal(self):
        # test
        with self.mysql.dao.SessionContext():
            exists = self.problem.update()
            
        # verify
        self.assertTrue(exists)
        with self.mysql.dao.create_session() as session:
            model = session.get(ProblemModel, 'thermometer.too_high')
            self.assertTrue(model.exists)
            
    def test_disabled(self):
        # set up
        with self.mysql.dao.create_session() as session:
            session.add(ProblemModel(name='thermometer.too_high', disabled=True, exists=False))
        
        # test
        with self.mysql.dao.SessionContext():
            exists = self.problem.update()
            
        # verify
        self.assertFalse(exists)
        with self.mysql.dao.create_session() as session:
            model = session.get(ProblemModel, 'thermometer.too_high')
            self.assertFalse(model.exists)
            