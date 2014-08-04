# -*- coding: utf-8 -*-
from atlantis.device import AbstractDevice, Sensor, Controller
from testutil import TestCase

class InvalidatesTest(TestCase):
    def test(self):
        # set up
        class PowerSensor(Sensor):
            def update(self):
                InvalidatesTest.called = True
        class TestDevice(AbstractDevice):
            power = PowerSensor()
            @Controller('power', invalidates='power')
            def on(self):
                pass
            
        # test
        device = TestDevice()
        device.on()
        self.assertTrue(self.called)
