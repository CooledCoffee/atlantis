# -*- coding: utf-8 -*-
from atlantis import device
from atlantis.device import Sensor, Controller, AbstractDevice
from fixtures._fixtures.monkeypatch import MonkeyPatch
from testutil import TestCase

class RegisterTest(TestCase):
    def test(self):
        self.useFixture(MonkeyPatch('atlantis.device.devices', {}))
        class ThermometerDevice(AbstractDevice):
            outer = Sensor()
            room = Sensor()
        self.assertEqual(1, len(device.devices))
        
class SensorsTest(TestCase):
    def test(self):
        class ThermometerDevice(AbstractDevice):
            outer = Sensor()
            room = Sensor()
        device = ThermometerDevice()
        self.assertEqual(2, len(device.sensors))
        self.assertEqual('outer', device.sensors[0].name)
        self.assertEqual('thermometer.outer', device.sensors[0].full_name)
        self.assertEqual('room', device.sensors[1].name)
        self.assertEqual('thermometer.room', device.sensors[1].full_name)
        
class ControllersTest(TestCase):
    def test(self):
        class SpeakerDevice(AbstractDevice):
            @Controller('power')
            def on(self):
                pass
            
            @Controller('power')
            def off(self):
                pass
        device = SpeakerDevice()
        controllers = device.controllers()
        self.assertEqual(2, len(controllers))
        self.assertEqual('off', controllers[0].name())
        self.assertEqual('speaker.off', controllers[0].full_name())
        self.assertEqual('on', controllers[1].name())
        self.assertEqual('speaker.on', controllers[1].full_name())
