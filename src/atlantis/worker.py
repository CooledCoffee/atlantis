# -*- coding: utf-8 -*-
from atlantis import device, rule

def update_sensors():
    for d in device.devices.values():
        for sensor in d.sensors:
            sensor = getattr(d, sensor)
            sensor.update()
            
def check_problems():
    return [p for p in rule.problems.values() if p.exists()]
    
def find_solutions(problem):
    candidates = rule.solutions[problem.name]
    return [c for c in candidates if c.feasible()]
