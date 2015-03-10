# -*- coding: utf-8 -*-
from atlantis import templates, device as mdevice
from decorated.base.dict import Dict
from metaweb import page

@page(path='/devices')
def devices():
    devices = mdevice.devices.values()
    devices.sort(key=lambda d: d.name)
    return templates.render('devices.html', devices=devices)

@page(path='/device')
def device(name):
    dev = mdevice.devices.get(name)
    return templates.render('device.html', device=dev)

@page(path='/rules')
def rules():
    problems = list(rule.problems.values())
    problems.sort(key=lambda p: p.name)
    items = [Dict(problem=p) for p in problems]
    for item in items:
        item.solutions = []
        for solution in rule.solutions.values():
            if type(item.problem) in solution.targets:
                item.solutions.append(solution)
        item.solutions.sort(key=lambda s: s.name)
    return templates.render('rules.html', items=items)
    