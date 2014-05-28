# -*- coding: utf-8 -*-
from atlantis import templates, rule, device as mdevice
from metaweb import page

@page
def devices():
    devices = mdevice.devices.values()
    devices.sort(key=lambda d: d.name)
    return templates.render('devices.html', devices=devices)

@page
def device(name):
    dev = mdevice.devices.get(name)
    return templates.render('device.html', device=dev)

@page
def rules():
    return templates.render('rules.html', problems=rule.problems,
            solutions=rule.solutions)
    