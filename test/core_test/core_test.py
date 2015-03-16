# -*- coding: utf-8 -*-
from atlantis import core
from atlantis.core.device import AbstractDevice
from atlantis.core.sensor import Sensor
from testutil import TestCase

class LocateCompTest(TestCase):
    def test(self):
        # set up
        class ThermometerDevice(AbstractDevice):
            @Sensor
            def room(self):
                return 25
            
        # test
        comp = core.clocate('thermometer.room')
        self.assertEqual('thermometer.room', comp.full_name())
        