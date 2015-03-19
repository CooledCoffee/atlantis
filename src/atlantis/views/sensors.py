# -*- coding: utf-8 -*-
from atlantis import core
from atlantis.db import SensorModel
from datetime import datetime
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
        'error_rate': model.error_rate if model is not None else 0,
        'name': name,
        'interval': sensor.interval,
        'time': model.time if model is not None else datetime(1970, 1, 1),
        'value': json.loads(model.value) if model is not None else None,
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
