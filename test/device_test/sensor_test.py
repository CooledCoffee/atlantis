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
        self.sensor.full_name = 'thermometer.room'
        self.sensor._retrieve = lambda: 25
        
class GetTest(SensorTest):
    def test_success(self):
        # set up
        self.useFixture(DateTimeFixture('atlantis.device.datetime', datetime(2000, 1, 1, 0, 0, 0)))
        with self.mysql.dao.create_session() as session:
            session.add(SensorModel(name='thermometer.room', value=json.dumps(25), time=datetime(2000, 1, 1)))
            
        # test
        with self.mysql.dao.SessionContext():
            self.assertEqual(25, self.sensor.value)
            self.assertEqual(datetime(2000, 1, 1), self.sensor.time)
            
    def test_expired(self):
        # set up
        with self.mysql.dao.create_session() as session:
            session.add(SensorModel(name='thermometer.room', value=json.dumps(25), time=datetime(2000, 1, 1)))
            
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
            sensor = session.get(SensorModel, 'thermometer.room')
            self.assertEqual(25, json.loads(sensor.value))
            self.assertEqual(datetime(2000, 1, 1), sensor.time)
        
class AvailableTest(SensorTest):
    def test_available(self):
        # set up
        with self.mysql.dao.create_session() as session:
            session.add(SensorModel(name='thermometer.room', value=25, time=datetime.now()))
            
        # test
        with self.mysql.dao.SessionContext():
            available = self.sensor.available()
            self.assertTrue(available)
            
    def test_outdated(self):
        # set up
        with self.mysql.dao.create_session() as session:
            session.add(SensorModel(name='thermometer.room', value=25, time=datetime(2000, 1, 1)))
            
        # test
        with self.mysql.dao.SessionContext():
            available = self.sensor.available()
            self.assertFalse(available)
            
    def test_no_record(self):
        with self.mysql.dao.SessionContext():
            available = self.sensor.available()
            self.assertFalse(available)
            
class UpdateTest(SensorTest):
    def test_normal(self):
        # test
        with self.mysql.dao.SessionContext():
            self.sensor.update()
            
        # verify
        with self.mysql.dao.create_session() as session:
            model = session.get(SensorModel, 'thermometer.room')
            self.assertEqual(25, json.loads(model.value))
            self.assertEqual(0, model.error_rate)
            
    def test_error(self):
        # set up
        def _retrieve():
            raise Exception()
        self.sensor._retrieve = _retrieve
        
        # test
        with self.mysql.dao.SessionContext():
            self.sensor.update()
            
        # verify
        with self.mysql.dao.create_session() as session:
            model = session.get(SensorModel, 'thermometer.room')
            self.assertIsNone(json.loads(model.value))
            self.assertEqual(0.000694444, model.error_rate)
    
    def test_almost_expired(self):
        # set up
        with self.mysql.dao.create_session() as session:
            time = datetime.now() - timedelta(seconds=55)
            session.add(SensorModel(name='thermometer.room', value=json.dumps(24), time=time))
            
        # test
        with self.mysql.dao.SessionContext():
            self.sensor.update()
            
        # verify
        with self.mysql.dao.create_session() as session:
            model = session.get(SensorModel, 'thermometer.room')
            self.assertEqual(25, json.loads(model.value))
            
    def test_not_expired(self):
        # set up
        with self.mysql.dao.create_session() as session:
            session.add(SensorModel(name='thermometer.room', value=json.dumps(24), time=datetime.now()))
            
        # test
        with self.mysql.dao.SessionContext():
            self.sensor.update()
            
        # verify
        with self.mysql.dao.create_session() as session:
            model = session.get(SensorModel, 'thermometer.room')
            self.assertEqual(24, json.loads(model.value))
            
    def test_force(self):
        # set up
        with self.mysql.dao.create_session() as session:
            session.add(SensorModel(name='thermometer.room', value=json.dumps(24), time=datetime.now()))
            
        # test
        with self.mysql.dao.SessionContext():
            self.sensor.update(force=True)
            
        # verify
        with self.mysql.dao.create_session() as session:
            model = session.get(SensorModel, 'thermometer.room')
            self.assertEqual(25, json.loads(model.value))
            
    def test_none_interval(self):
        # set up
        with self.mysql.dao.create_session() as session:
            session.add(SensorModel(name='thermometer.room', value=json.dumps(24), time=datetime(2000, 1, 1)))
        self.sensor.interval = None
            
        # test
        with self.mysql.dao.SessionContext():
            self.sensor.update()
            
        # verify
        with self.mysql.dao.create_session() as session:
            model = session.get(SensorModel, 'thermometer.room')
            self.assertEqual(24, json.loads(model.value))
            self.assertEqual(datetime(2000, 1, 1), model.time)
            