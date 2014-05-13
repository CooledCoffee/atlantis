# -*- coding: utf-8 -*-
from atlantis import device

def update_sensors():
    for d in device.devices.values():
        for sensor in d.sensors:
            sensor = getattr(d, sensor)
            sensor.update()
            