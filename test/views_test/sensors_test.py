# -*- coding: utf-8 -*-
from atlantis.views import sensors
from datetime import datetime
from decorated.base.dict import Dict
from testutil import TestCase

class GetTest(TestCase):
    def test(self):
        sensor = Dict(value=25, time=datetime(2000, 1, 1))
        self.patches.patch('atlantis.device.devices', {'thermometer': Dict(temperature=sensor)})
        result = sensors.get('thermometer.temperature')
        self.assertEqual(datetime(2000, 1, 1), result['time'])
        self.assertEqual(25, result['value'])
    