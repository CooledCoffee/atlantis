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
    problem_class = type(problem)
    candidates = [s for s in rule.solutions.values() if problem_class in s.targets]
    return [c for c in candidates if c._fitness() > 0]
