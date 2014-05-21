# -*- coding: utf-8 -*-
from atlantis.db import SensorModel
from atlantis.device import Device, Sensor
from atlantis.views import sensors
from datetime import datetime
from fixtures2 import DateTimeFixture
from testutil import DbTestCase, TestCase
import json

class TemperatureSensor(Sensor):
    def retrieve(self):
        return 25
    
class ThermometerDevice(Device):
    temperature = TemperatureSensor()

class GetTest(DbTestCase):
    def test(self):
        # set up
        self.useFixture(DateTimeFixture('atlantis.device.datetime', datetime(2000, 1, 1)))
        with self.mysql.dao.create_session() as session:
            session.add(SensorModel(name='thermometer.temperature', value=json.dumps(25), time=datetime(2000, 1, 1)))
            
        # test
        with self.mysql.dao.SessionContext():
            result = sensors.get('thermometer.temperature')
        self.assertEqual(datetime(2000, 1, 1), result['time'])
        self.assertEqual(25, result['value'])
    
class SetTest(DbTestCase):
    def test(self):
        # set up
        self.useFixture(DateTimeFixture('atlantis.device.datetime', datetime(2000, 1, 1)))
        
        # test
        with self.mysql.dao.SessionContext():
            sensors.set('thermometer.temperature', 25)
        with self.mysql.dao.create_session() as session:
            model = session.get(SensorModel, 'thermometer.temperature')
            self.assertEqual(25, json.loads(model.value))
            self.assertEqual(datetime(2000, 1, 1), model.time)
            
class RetrieveTest(TestCase):
    def test(self):
        result = sensors.retrieve('thermometer.temperature')
        self.assertEqual(25, result)
