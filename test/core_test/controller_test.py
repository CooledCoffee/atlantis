# -*- coding: utf-8 -*-
from atlantis.core.controller import Controller
from atlantis.core.device import AbstractDevice
from atlantis.core.sensor import Sensor
from testutil import TestCase

class InvalidatesTest(TestCase):
    def test(self):
        # set up
        class TestDevice(AbstractDevice):
            @Sensor
            def power(self):
                InvalidatesTest.power = True
            
            @Controller('power', invalidate='power')
            def on(self):
                pass
            
        # test
        device = TestDevice()
        device.on.trigger()
        self.assertTrue(self.power)
