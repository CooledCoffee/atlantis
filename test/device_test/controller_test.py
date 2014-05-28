# -*- coding: utf-8 -*-
from atlantis.device import Device, Sensor, Controller
from testutil import TestCase

class AffectsTest(TestCase):
    def test(self):
        # set up
        class PowerSensor(Sensor):
            def update(self):
                AffectsTest.updated = True
        class TestDevice(Device):
            power = PowerSensor()
            @Controller('power', affects='power')
            def on(self):
                pass
            
        # test
        device = TestDevice()
        device.on()
        self.assertTrue(self.updated)
