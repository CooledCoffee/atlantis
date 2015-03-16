# -*- coding: utf-8 -*-
from atlantis import templates, core
from metaweb import page

@page(path='/')
def devices():
    devices = core.devices.values()
    devices.sort(key=lambda d: d.name)
    return templates.render('devices.html', devices=devices)

@page(path='/device')
def device(name):
    dev = core.devices.get(name)
    return templates.render('device.html', device=dev)
