# -*- coding: utf-8 -*-
from atlantis import device
from metaweb import api

@api
def get(name):
    dname, sname = name.split('.')
    dev = device.devices[dname]
    sensor = getattr(dev, sname)
    return {
        'time': sensor.time,
        'value': sensor.value,
    }
