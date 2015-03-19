# -*- coding: utf-8 -*-
from atlantis.db import SensorModel
from atlantis.core.device import AbstractDevice, Sensor
from atlantis.views import sensors
from datetime import datetime
from fixtures2 import DateTimeFixture
from testutil import DbTestCase
import json

class GetTest(DbTestCase):
    def test_success(self):
        # set up
        class ThermometerDevice(AbstractDevice):
            @Sensor
            def room(self):
                return 25
        with self.mysql.dao.create_session() as session:
            sensor = SensorModel(name='thermometer.room',
                    error_rate=0.01,
                    value=json.dumps(25),
                    time=datetime(2000, 1, 1))
            session.add(sensor)
            
        # test
        with self.mysql.dao.SessionContext():
            result = sensors.get('thermometer.room')
        self.assertEqual('thermometer.room', result['name'])
        self.assertEqual(0.01, result['error_rate'])
        self.assertEqual(60, result['interval'])
        self.assertEqual(datetime(2000, 1, 1), result['time'])
        self.assertEqual(25, result['value'])
        
    def test_model_not_exists(self):
        # set up
        class ThermometerDevice(AbstractDevice):
            @Sensor
            def room(self):
                return 25
            
        # test
        with self.mysql.dao.SessionContext():
            result = sensors.get('thermometer.room')
        self.assertEqual('thermometer.room', result['name'])
        self.assertEqual(0, result['error_rate'])
        self.assertEqual(60, result['interval'])
        self.assertEqual(datetime(1970, 1, 1), result['time'])
        self.assertIsNone(result['value'])
    
class AllTest(DbTestCase):
    def test(self):
        # set up
        class ThermometerDevice(AbstractDevice):
            @Sensor
            def room(self):
                return 25
        with self.mysql.dao.create_session() as session:
            sensor = SensorModel(name='thermometer.room',
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
        self.useFixture(DateTimeFixture('atlantis.core.sensor.datetime', datetime(2000, 1, 1)))
        class ThermometerDevice(AbstractDevice):
            @Sensor
            def room(self):
                return 25
        
        # test
        with self.mysql.dao.SessionContext():
            sensors.set('thermometer.room', 25)
        with self.mysql.dao.create_session() as session:
            model = session.get(SensorModel, 'thermometer.room')
            self.assertEqual(25, json.loads(model.value))
            self.assertEqual(datetime(2000, 1, 1), model.time)
            
class UpdateTest(DbTestCase):
    def test(self):
        # set up
        self.useFixture(DateTimeFixture('atlantis.core.sensor.datetime', datetime(2000, 1, 1)))
        class ThermometerDevice(AbstractDevice):
            @Sensor
            def room(self):
                return 25
        
        # test
        with self.mysql.dao.SessionContext():
            result = sensors.update('thermometer.room')
            self.assertEqual(25, result['value'])
            self.assertEqual(datetime(2000, 1, 1), result['time'])
