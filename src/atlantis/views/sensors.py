# -*- coding: utf-8 -*-
from atlantis import device
from atlantis.db import SensorModel
from decorated.base.context import ctx
from metaweb import api

@api
def get(name):
    sensor = _get_sensor(name)
    model = ctx.session.get(SensorModel, name)
    return {
        'error_rate': model.error_rate,
        'interval': sensor.interval,
        'time': sensor.time,
        'value': sensor.value,
    }
    
@api
def update(name):
    sensor = _get_sensor(name)
    sensor.update(force=True)
    return get(name)

@api
def set(name, value):
    sensor = _get_sensor(name)
    sensor.value = value

def _get_sensor(name):
    dname, sname = name.split('.')
    dev = device.devices[dname]
    return getattr(dev, sname)
    