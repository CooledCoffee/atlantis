# -*- coding: utf-8 -*-
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
    def test(self):
        # set up
        sensor = Sensor()
        sensor._device = Dict(name='thermometer')
        sensor._name = 'temperature'
        sensor._retrieve = lambda: 25
        
        # test
        with self.mysql.dao.SessionContext():
            sensor.update()
        with self.mysql.dao.SessionContext():
            self.assertEqual(25, sensor.value)
    