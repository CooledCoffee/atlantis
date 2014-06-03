# -*- coding: utf-8 -*-
from atlantis.db import SensorModel
from atlantis.device import AbstractDevice, Sensor
from atlantis.views import sensors
from datetime import datetime
from fixtures2 import DateTimeFixture
from testutil import DbTestCase
import json

class GetTest(DbTestCase):
    def test(self):
        # set up
        self.useFixture(DateTimeFixture('atlantis.device.datetime', datetime(2000, 1, 1)))
        self.patches.patch('atlantis.device.devices', {})
        class TemperatureSensor(Sensor):
            def _retrieve(self):
                return 25
        class ThermometerDevice(AbstractDevice):
            temperature = TemperatureSensor()
        with self.mysql.dao.create_session() as session:
            sensor = SensorModel(name='thermometer.temperature',
                    error_rate=0.01,
                    value=json.dumps(25),
                    time=datetime(2000, 1, 1))
            session.add(sensor)
            
        # test
        with self.mysql.dao.SessionContext():
            result = sensors.get('thermometer.temperature')
        self.assertEqual('thermometer.temperature', result['name'])
        self.assertEqual(0.01, result['error_rate'])
        self.assertEqual(60, result['interval'])
        self.assertEqual(datetime(2000, 1, 1), result['time'])
        self.assertEqual(25, result['value'])
    
class AllTest(DbTestCase):
    def test(self):
        # set up
        self.useFixture(DateTimeFixture('atlantis.device.datetime', datetime(2000, 1, 1)))
        self.patches.patch('atlantis.device.devices', {})
        class TemperatureSensor(Sensor):
            def _retrieve(self):
                return 25
        class ThermometerDevice(AbstractDevice):
            temperature = TemperatureSensor()
        with self.mysql.dao.create_session() as session:
            sensor = SensorModel(name='thermometer.temperature',
                    error_rate=0.01,
                    value=json.dumps(25),
                    time=datetime(2000, 1, 1))
            session.add(sensor)
            
        # test
        with self.mysql.dao.SessionContext():
            results = sensors.all()
        self.assertEqual(1, len(results))
        self.assertEqual(0.01, results[0]['error_rate'])
        self.assertEqual(60, results[0]['interval'])
        self.assertEqual(datetime(2000, 1, 1), results[0]['time'])
        self.assertEqual(25, results[0]['value'])
        
class SetTest(DbTestCase):
    def test(self):
        # set up
        self.useFixture(DateTimeFixture('atlantis.device.datetime', datetime(2000, 1, 1)))
        self.patches.patch('atlantis.device.devices', {})
        class TemperatureSensor(Sensor):
            def _retrieve(self):
                return 25
        class ThermometerDevice(AbstractDevice):
            temperature = TemperatureSensor()
        
        # test
        with self.mysql.dao.SessionContext():
            sensors.set('thermometer.temperature', 25)
        with self.mysql.dao.create_session() as session:
            model = session.get(SensorModel, 'thermometer.temperature')
            self.assertEqual(25, json.loads(model.value))
            self.assertEqual(datetime(2000, 1, 1), model.time)
            
class UpdateTest(DbTestCase):
    def test(self):
        # set up
        self.useFixture(DateTimeFixture('atlantis.device.datetime', datetime(2000, 1, 1)))
        self.patches.patch('atlantis.device.devices', {})
        class TemperatureSensor(Sensor):
            def _retrieve(self):
                return 25
        class ThermometerDevice(AbstractDevice):
            temperature = TemperatureSensor()
        
        # test
        with self.mysql.dao.SessionContext():
            result = sensors.update('thermometer.temperature')
            self.assertEqual(25, result['value'])
            self.assertEqual(datetime(2000, 1, 1), result['time'])
