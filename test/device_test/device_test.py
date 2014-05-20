# -*- coding: utf-8 -*-
from atlantis import device
from atlantis.device import Device, Sensor, Controller
from fixtures._fixtures.monkeypatch import MonkeyPatch
from fixtures2 import TestCase

class RegisterTest(TestCase):
    def test(self):
        self.useFixture(MonkeyPatch('atlantis.device.devices', {}))
        class TestDevice(Device):
            humidity = Sensor()
            temperature = Sensor()
        self.assertEqual(1, len(device.devices))
        
class SensorsTest(TestCase):
    def test(self):
        class TestDevice(Device):
            humidity = Sensor()
            temperature = Sensor()
        device = TestDevice()
        self.assertEqual(2, len(device.sensors))
        self.assertEqual('humidity', device.sensors[0].name)
        self.assertEqual('test.humidity', device.sensors[0].full_name)
        self.assertEqual('temperature', device.sensors[1].name)
        self.assertEqual('test.temperature', device.sensors[1].full_name)
        
class ControllersTest(TestCase):
    def test(self):
        class TestDevice(Device):
            @Controller('power')
            def on(self):
                pass
            
            @Controller('power')
            def off(self):
                pass
        device = TestDevice()
        self.assertEqual(2, len(device.controllers))
        self.assertEqual('off', device.controllers[0].name)
        self.assertEqual('test.off', device.controllers[0].full_name)
        self.assertEqual('on', device.controllers[1].name)
        self.assertEqual('test.on', device.controllers[1].full_name)
