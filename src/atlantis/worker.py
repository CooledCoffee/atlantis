# -*- coding: utf-8 -*-
from atlantis import device, rule
from atlantis.db import SolutionModel
from decorated.base.context import ctx

def _update_sensors():
    for d in device.devices.values():
        for sensor in d.sensors:
            sensor = getattr(d, sensor)
            sensor.update()
            
def _update_solution_statuses():
    models = ctx.session.query(SolutionModel) \
            .filter(SolutionModel.applied == True) \
            .all()
    for model in models:
        solution = rule.solutions[model.name]
        solution.update()
        
def _check_problems():
    return [p for p in rule.problems.values() if p.check()]
    
def _find_best_solution(problem):
    problem_class = type(problem)
    candidates = [s for s in rule.solutions.values() if problem_class in s.targets]
    solutions = [c for c in candidates if c._fitness() > 0]
    return solutions[0] if len(solutions) > 0 else None
