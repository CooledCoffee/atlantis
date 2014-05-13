# -*- coding: utf-8 -*-
from atlantis import worker, device
from atlantis.db import Sensor as SensorModel
from atlantis.device import Device, Sensor
from fixtures._fixtures.monkeypatch import MonkeyPatch
from testutil import DbTestCase
import json

class UpdateSensorsTest(DbTestCase):
    def test(self):
        # set up
        self.useFixture(MonkeyPatch('atlantis.device.devices', {}))
        class ThermometerDevice(Device):
            temperature = Sensor()
        class HydrometerDevice(Device):
            humidity = Sensor()
        device.devices['thermometer'].temperature._retrieve = lambda: 25
        device.devices['hydrometer'].humidity._retrieve = lambda: 50
        
        # test
        with self.mysql.dao.SessionContext():
            worker.update_sensors()
        with self.mysql.dao.create_session() as session:
            sensors = session.query(SensorModel).all()
            self.assertEqual(2, len(sensors))
            self.assertEqual('hydrometer.humidity', sensors[0].name)
            self.assertEqual(50, json.loads(sensors[0].value))
            self.assertEqual('thermometer.temperature', sensors[1].name)
            self.assertEqual(25, json.loads(sensors[1].value))
            