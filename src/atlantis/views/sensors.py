# -*- coding: utf-8 -*-
from atlantis import device
from metaweb import api

@api
def get(name):
    sensor = _get_sensor(name)
    return {
        'time': sensor.time,
        'value': sensor.value,
    }
    
@api
def retrieve(name):
    sensor = _get_sensor(name)
    return sensor.retrieve()

@api
def set(name, value):
    sensor = _get_sensor(name)
    sensor.value = value

def _get_sensor(name):
    dname, sname = name.split('.')
    dev = device.devices[dname]
    return getattr(dev, sname)
    