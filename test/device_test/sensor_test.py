# -*- coding: utf-8 -*-
from atlantis.db import SensorModel
from atlantis.device import Sensor
from datetime import datetime, timedelta
from fixtures2 import DateTimeFixture
from testutil import DbTestCase
import json

class SensorTest(DbTestCase):
    def setUp(self):
        super(SensorTest, self).setUp()
        self.sensor = Sensor()
        self.sensor.full_name = 'thermometer.temperature'
        self.sensor.retrieve = lambda: 25
        
class GetTest(SensorTest):
    def test_success(self):
        # set up
        self.useFixture(DateTimeFixture('atlantis.device.datetime', datetime(2000, 1, 1, 0, 0, 0)))
        with self.mysql.dao.create_session() as session:
            session.add(SensorModel(name='thermometer.temperature', value=json.dumps(25), time=datetime(2000, 1, 1)))
            
        # test
        with self.mysql.dao.SessionContext():
            self.assertEqual(25, self.sensor.value)
            self.assertEqual(datetime(2000, 1, 1), self.sensor.time)
            
    def test_expired(self):
        # set up
        with self.mysql.dao.create_session() as session:
            session.add(SensorModel(name='thermometer.temperature', value=json.dumps(25), time=datetime(2000, 1, 1)))
            
        # test
        with self.mysql.dao.SessionContext():
            self.assertIsNone(self.sensor.value)
            self.assertEqual(datetime(2000, 1, 1), self.sensor.time)
            
    def test_no_record(self):
        # test
        with self.mysql.dao.SessionContext():
            self.assertIsNone(self.sensor.value)
            self.assertEqual(datetime(1970, 1, 1), self.sensor.time)
            
class SetTest(SensorTest):
    def test(self):
        # set up
        self.useFixture(DateTimeFixture('atlantis.device.datetime', datetime(2000, 1, 1, 0, 0, 0)))
        
        # test
        with self.mysql.dao.SessionContext():
            self.sensor.value = 25
            
        # verify
        with self.mysql.dao.create_session() as session:
            sensor = session.get(SensorModel, 'thermometer.temperature')
            self.assertEqual(25, json.loads(sensor.value))
            self.assertEqual(datetime(2000, 1, 1), sensor.time)
        
class AvailableTest(SensorTest):
    def test_available(self):
        # set up
        with self.mysql.dao.create_session() as session:
            session.add(SensorModel(name='thermometer.temperature', value=25, time=datetime.now()))
            
        # test
        with self.mysql.dao.SessionContext():
            available = self.sensor.available()
            self.assertTrue(available)
            
    def test_outdated(self):
        # set up
        with self.mysql.dao.create_session() as session:
            session.add(SensorModel(name='thermometer.temperature', value=25, time=datetime(2000, 1, 1)))
            
        # test
        with self.mysql.dao.SessionContext():
            available = self.sensor.available()
            self.assertFalse(available)
            
    def test_no_record(self):
        with self.mysql.dao.SessionContext():
            available = self.sensor.available()
            self.assertFalse(available)
            
class UpdateTest(SensorTest):
    def test_expired(self):
        # test
        with self.mysql.dao.SessionContext():
            self.sensor.update()
            
        # verify
        with self.mysql.dao.create_session() as session:
            model = session.get(SensorModel, 'thermometer.temperature')
            self.assertEqual(25, json.loads(model.value))
    
    def test_almost_expired(self):
        # set up
        with self.mysql.dao.create_session() as session:
            time = datetime.now() - timedelta(seconds=55)
            session.add(SensorModel(name='thermometer.temperature', value=json.dumps(24), time=time))
            
        # test
        with self.mysql.dao.SessionContext():
            self.sensor.update()
            
        # verify
        with self.mysql.dao.create_session() as session:
            model = session.get(SensorModel, 'thermometer.temperature')
            self.assertEqual(25, json.loads(model.value))
            
    def test_no_update(self):
        # set up
        with self.mysql.dao.create_session() as session:
            time = datetime.now() - timedelta(seconds=55)
            session.add(SensorModel(name='thermometer.temperature', value=json.dumps(24), time=time))
        self.sensor.retrieve = lambda: None
            
        # test
        with self.mysql.dao.SessionContext():
            self.sensor.update()
            
        # verify
        with self.mysql.dao.create_session() as session:
            model = session.get(SensorModel, 'thermometer.temperature')
            self.assertEqual(24, json.loads(model.value))
    
    def test_not_expired(self):
        # set up
        with self.mysql.dao.create_session() as session:
            session.add(SensorModel(name='thermometer.temperature', value=json.dumps(24), time=datetime.now()))
            
        # test
        with self.mysql.dao.SessionContext():
            self.sensor.update()
            
        # verify
        with self.mysql.dao.create_session() as session:
            model = session.get(SensorModel, 'thermometer.temperature')
            self.assertEqual(24, json.loads(model.value))
            
    def test_force(self):
        # set up
        with self.mysql.dao.create_session() as session:
            session.add(SensorModel(name='thermometer.temperature', value=json.dumps(24), time=datetime.now()))
            
        # test
        with self.mysql.dao.SessionContext():
            self.sensor.update(force=True)
            
        # verify
        with self.mysql.dao.create_session() as session:
            model = session.get(SensorModel, 'thermometer.temperature')
            self.assertEqual(25, json.loads(model.value))
            