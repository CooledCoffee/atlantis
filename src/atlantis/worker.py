# -*- coding: utf-8 -*-
from atlantis import device, rule
from atlantis.db import SolutionModel
from decorated.base.context import ctx
from loggingd import log_enter, log_return

def run():
    _update_sensors()
    _update_solution_statuses()
    problems = _check_problems()
    for problem in problems:
        solution = _find_best_solution(problem)
        solution.apply()

@log_enter('Updating sensors ...')
def _update_sensors():
    for d in device.devices.values():
        for sensor in d.sensors:
            sensor = getattr(d, sensor)
            sensor.update()
            
@log_enter('Updating solution statuses ...')
def _update_solution_statuses():
    models = ctx.session.query(SolutionModel) \
            .filter(SolutionModel.applied == True) \
            .all()
    for model in models:
        solution = rule.solutions[model.name]
        solution.update()
        
@log_enter('Checking problems ...')
def _check_problems():
    return [p for p in rule.problems.values() if p.check()]
    
@log_enter('Solving problem {problem.name} ...')
@log_return('Found solution {ret.name}.', condition='ret is not None')
@log_return('No solution.', condition='ret is None')
def _find_best_solution(problem):
    problem_class = type(problem)
    candidates = [s for s in rule.solutions.values() if problem_class in s.targets]
    solutions = [c for c in candidates if c.check() > 0]
    return solutions[0] if len(solutions) > 0 else None
