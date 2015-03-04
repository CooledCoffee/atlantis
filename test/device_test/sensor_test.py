# -*- coding: utf-8 -*-
from atlantis.base import ExpiredError
from atlantis.db import SensorModel
from atlantis.device import Sensor, AbstractDevice
from datetime import datetime, timedelta
from fixtures2 import DateTimeFixture
from testutil import DbTestCase
import json

class SensorTest(DbTestCase):
    def setUp(self):
        super(SensorTest, self).setUp()
        class ThermometerDevice(AbstractDevice):
            @Sensor
            def room(self):
                return 25
        self.sensor = ThermometerDevice().room
        
class GetTest(SensorTest):
    def test_success(self):
        # set up
        self.useFixture(DateTimeFixture('atlantis.device.datetime', datetime(2000, 1, 1, 0, 0, 0)))
        with self.mysql.dao.create_session() as session:
            session.add(SensorModel(name='thermometer.room', value=json.dumps(25), time=datetime(2000, 1, 1)))
            
        # test
        with self.mysql.dao.SessionContext():
            self.assertEqual(25, self.sensor.value())
            self.assertEqual(datetime(2000, 1, 1), self.sensor.time())
            
    def test_expired(self):
        # set up
        with self.mysql.dao.create_session() as session:
            session.add(SensorModel(name='thermometer.room', value=json.dumps(25), time=datetime(2000, 1, 1)))
            
        # test
        with self.mysql.dao.SessionContext():
            self.assertEqual(datetime(2000, 1, 1), self.sensor.time())
            with self.assertRaises(ExpiredError):
                self.sensor.value()
             
    def test_no_record(self):
        # test
        with self.mysql.dao.SessionContext():
            self.assertEqual(datetime(1970, 1, 1), self.sensor.time())
            with self.assertRaises(ExpiredError):
                self.sensor.value()
            
class SetTest(SensorTest):
    def test(self):
        # set up
        self.useFixture(DateTimeFixture('atlantis.device.datetime', datetime(2000, 1, 1, 0, 0, 0)))
        
        # test
        with self.mysql.dao.SessionContext():
            self.sensor.value(25)
            
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
            
    def test_no_interval(self):
        # set up
        class ThermometerDevice(AbstractDevice):
            @Sensor(interval=None)
            def room(self):
                return 25
        self.sensor.interval = None
        with self.mysql.dao.create_session() as session:
            session.add(SensorModel(name='thermometer.room', value=25, time=datetime(2000, 1, 1)))
            
        # test
        with self.mysql.dao.SessionContext():
            available = ThermometerDevice().room.available()
            self.assertTrue(available)
            
class ShouldUpdateTest(SensorTest):
    def test_expired(self):
        # set up
        with self.mysql.dao.create_session() as session:
            session.add(SensorModel(name='thermometer.room', value=25, time=datetime.now() - timedelta(seconds=120)))
        
        # test
        with self.mysql.dao.SessionContext():
            result = self.sensor.should_update()
            self.assertTrue(result)
            
    def test_almost_expired(self):
        # set up
        with self.mysql.dao.create_session() as session:
            session.add(SensorModel(name='thermometer.room', value=25, time=datetime.now() - timedelta(seconds=55)))
            
        # test
        with self.mysql.dao.SessionContext():
            result = self.sensor.should_update()
            self.assertTrue(result)
            
    def test_not_expired(self):
        # set up
        with self.mysql.dao.create_session() as session:
            session.add(SensorModel(name='thermometer.room', value=25, time=datetime.now() - timedelta(seconds=30)))
            
        # test
        with self.mysql.dao.SessionContext():
            result = self.sensor.should_update()
            self.assertFalse(result)
        
    def test_no_interval(self):
        # set up
        class ThermometerDevice(AbstractDevice):
            @Sensor(interval=None)
            def room(self):
                return 25
        with self.mysql.dao.create_session() as session:
            session.add(SensorModel(name='thermometer.room', value=25, time=datetime.now() - timedelta(seconds=3600)))
             
        # test
        with self.mysql.dao.SessionContext():
            result = ThermometerDevice().room.should_update()
            self.assertFalse(result)
            
class UpdateTest(SensorTest):
    def setUp(self):
        super(UpdateTest, self).setUp()
        self.useFixture(DateTimeFixture('atlantis.device.datetime', datetime(2000, 1, 1, 0, 0, 0)))
        
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
        class ThermometerDevice(AbstractDevice):
            @Sensor
            def room(self):
                raise Exception()
        
        # test
        with self.mysql.dao.SessionContext():
            ThermometerDevice().room.update()
            
        # verify
        with self.mysql.dao.create_session() as session:
            model = session.get(SensorModel, 'thermometer.room')
            self.assertIsNone(json.loads(model.value))
            self.assertEqual(0.000694444, model.error_rate)
        