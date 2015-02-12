# -*- coding: utf-8 -*-
from atlantis.device import AutoNameComponent, AbstractDevice
from fixtures2 import TestCase

class AutoNameComponentTest(TestCase):
    def test(self):
        class ThermometerDevice(AbstractDevice):
            @AutoNameComponent
            def room(self):
                pass
        thermometer = ThermometerDevice()
        self.assertEqual('room', thermometer.room.name())
        self.assertEqual('thermometer.room', thermometer.room.full_name())
        