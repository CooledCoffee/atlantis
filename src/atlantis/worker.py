# -*- coding: utf-8 -*-
from atlantis import device, rule

def _update_sensors():
    for d in device.devices.values():
        for sensor in d.sensors:
            sensor = getattr(d, sensor)
            sensor.update()
            
def _check_problems():
    return [p for p in rule.problems.values() if p.check()]
    
def _find_solutions(problem):
    candidates = rule.solutions[problem.name]
    return [c for c in candidates if c._fitness() > 0]
