# -*- coding: utf-8 -*-
from atlantis import core
from atlantis.db import SensorModel
from decorated.base.context import ctx
from metaweb import api
import json

@api
def all():
    results = []
    for dev in core.devices.values():
        for sensor in dev.sensors():
            result = get(sensor.full_name())
            results.append(result)
    results.sort(key=lambda r: r['name'])
    return results

@api
def get(name):
    sensor = core.clocate(name)
    model = ctx.session.get(SensorModel, name)
    return {
        'error_rate': model.error_rate,
        'name': name,
        'interval': sensor.interval,
        'time': model.time,
        'value': json.loads(model.value),
    }
    
@api
def update(name):
    sensor = core.clocate(name)
    sensor.update()
    return get(name)

@api
def set(name, value):
    sensor = core.clocate(name)
    sensor.value(value)
