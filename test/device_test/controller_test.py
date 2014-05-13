# -*- coding: utf-8 -*-
from atlantis.device import Device, Sensor, controller
from fixtures2 import TestCase

class AffectsTest(TestCase):
    def test(self):
        # set up
        case = self
        class PowerSensor(Sensor):
            def update(self):
                case.updated = True
        class TestDevice(Device):
            power = PowerSensor()
            @controller(affects='power')
            def on(self):
                pass
            
        # test
        device = TestDevice()
        device.on()
        self.assertTrue(self.updated)
