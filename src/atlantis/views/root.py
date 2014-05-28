# -*- coding: utf-8 -*-
from atlantis import templates, device, rule
from metaweb import page

@page
def devices():
    devices = device.devices.values()
    devices.sort(key=lambda d: d.name)
    return templates.render('devices.html', devices=devices)

@page
def device(name):
    dev = device.devices.get(name)
    return templates.render('device.html', device=dev)

@page
def rules():
    return templates.render('rules.html', problems=rule.problems,
            solutions=rule.solutions)
    