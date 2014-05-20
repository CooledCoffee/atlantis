# -*- coding: utf-8 -*-
from atlantis import templates, device
from metaweb import page

@page(default=True)
def home():
    devices = device.devices.values()
    devices.sort(key=lambda d: d.name)
    return templates.render('devices.html', devices=devices)
