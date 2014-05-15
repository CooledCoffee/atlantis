# -*- coding: utf-8 -*-
from atlantis import device
from atlantis.device import Device, Sensor, controller
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
        self.assertEqual(['humidity', 'temperature'], device.sensors)
        self.assertEqual('humidity', device.humidity.name)
        self.assertEqual('test.humidity', device.humidity.full_name)
        
class ControllersTest(TestCase):
    def test(self):
        class TestDevice(Device):
            @controller
            def on(self):
                pass
            
            @controller
            def off(self):
                pass
        device = TestDevice()
        self.assertEqual(['off', 'on'], device.controllers)
        self.assertEqual('on', device.on.name)
        self.assertEqual('test.on', device.on.full_name)
