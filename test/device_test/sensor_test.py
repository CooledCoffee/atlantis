# -*- coding: utf-8 -*-
from atlantis.db import Sensor as SensorModel
from atlantis.device import Sensor
from datetime import datetime
from decorated.base.dict import Dict
from fixtures2 import DateTimeFixture
from testutil import DbTestCase

class GetSetTest(DbTestCase):
    def test(self):
        # set up
        self.useFixture(DateTimeFixture('atlantis.device.datetime', datetime(2000, 1, 1, 0, 0, 0)))
        sensor = Sensor()
        sensor._device = Dict(name='thermometer')
        sensor._name = 'temperature'
        
        # test
        with self.mysql.dao.SessionContext():
            sensor.value = 25
        with self.mysql.dao.SessionContext():
            self.assertEqual(25, sensor.value)
            self.assertEqual(datetime(2000, 1, 1, 0, 0, 0), sensor.time)

class UpdateTest(DbTestCase):
    def setUp(self):
        super(UpdateTest, self).setUp()
        self.sensor = Sensor()
        self.sensor.name = 'temperature'
        self.sensor._device = Dict(name='thermometer')
        self.sensor._retrieve = lambda: 25
        
    def test_expired(self):
        with self.mysql.dao.SessionContext():
            self.sensor.update()
        with self.mysql.dao.SessionContext():
            self.assertEqual(25, self.sensor.value)
    
    def test_not_expired(self):
        # set up
        with self.mysql.dao.create_session() as session:
            session.add(SensorModel(name='thermometer.temperature', value=24, time=datetime.now()))
            
        # test
        with self.mysql.dao.SessionContext():
            self.sensor.update()
        with self.mysql.dao.SessionContext():
            self.assertEqual(24, self.sensor.value)
    
    def test_force(self):
        # set up
        with self.mysql.dao.create_session() as session:
            session.add(SensorModel(name='thermometer.temperature', value=24, time=datetime.now()))
            
        # test
        with self.mysql.dao.SessionContext():
            self.sensor.update(force=True)
        with self.mysql.dao.SessionContext():
            self.assertEqual(25, self.sensor.value)
            