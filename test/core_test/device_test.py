# -*- coding: utf-8 -*-
from atlantis import core
from atlantis.core import device
from atlantis.core.device import Sensor, AbstractDevice
from testutil import TestCase

class RegisterTest(TestCase):
    def test(self):
        class ThermometerDevice(AbstractDevice):
            pass
        self.assertEqual(1, len(core.devices))
        
class ListComponentsTest(TestCase):
    def test(self):
        class ThermometerDevice(AbstractDevice):
            @Sensor
            def outer(self):
                return 20
            
            @Sensor
            def room(self):
                return 25
        sensors = ThermometerDevice()._list_components(Sensor)
        self.assertEqual(2, len(sensors))
        self.assertEqual('outer', sensors[0].name())
        self.assertEqual('thermometer.outer', sensors[0].full_name())
        self.assertEqual('room', sensors[1].name())
        self.assertEqual('thermometer.room', sensors[1].full_name())
