# -*- coding: utf-8 -*-
from atlantis.controller import Controller
from atlantis.device import AbstractDevice
from atlantis.sensor import Sensor
from testutil import TestCase

class InvalidatesTest(TestCase):
    def test(self):
        # set up
        class TestDevice(AbstractDevice):
            @Sensor
            def power(self):
                InvalidatesTest.power = True
            
            @Controller('power', invalidates='power')
            def on(self):
                pass
            
        # test
        device = TestDevice()
        device.on.trigger()
        self.assertTrue(self.power)
