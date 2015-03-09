# -*- coding: utf-8 -*-
from atlantis.base import DeviceComponent
from atlantis.db import SensorModel, ProblemModel
from atlantis.device import AbstractDevice
from fixtures2 import TestCase
from testutil import DbTestCase

class NameTest(TestCase):
    def test(self):
        class ThermometerDevice(AbstractDevice):
            @DeviceComponent
            def room(self):
                pass
        thermometer = ThermometerDevice()
        self.assertEqual('room', thermometer.room.name())
        self.assertEqual('thermometer.room', thermometer.room.full_name())
        
class GetModelTest(DbTestCase):
    def test(self):
        # set up
        class Sensor(DeviceComponent):
            pass
        class ThermometerDevice(AbstractDevice):
            @Sensor
            def room(self):
                pass
        with self.mysql.dao.create_session() as session:
            session.add(SensorModel(name='thermometer.room'))
            
        # test
        with self.mysql.dao.SessionContext():
            model = ThermometerDevice().room._get_model()
            self.assertEqual('thermometer.room', model.name)
            
class GetBoolFieldTest(DbTestCase):
    def setUp(self):
        super(GetBoolFieldTest, self).setUp()
        class Problem(DeviceComponent):
            pass
        class ThermometerDevice(AbstractDevice):
            @Problem
            def room(self):
                pass
        self.comp = ThermometerDevice().room
        
    def test_true(self):
        # set up
        with self.mysql.dao.create_session() as session:
            session.add(ProblemModel(name='thermometer.room', exists=True))
            
        # test
        with self.mysql.dao.SessionContext():
            result = self.comp._get_bool_field('exists')
            self.assertTrue(result)
            
    def test_false(self):
        # set up
        with self.mysql.dao.create_session() as session:
            session.add(ProblemModel(name='thermometer.room', exists=False))
            
        # test
        with self.mysql.dao.SessionContext():
            result = self.comp._get_bool_field('exists')
            self.assertFalse(result)
            
    def test_no_record(self):
        # test
        with self.mysql.dao.SessionContext():
            result = self.comp._get_bool_field('exists')
            self.assertFalse(result)
            