# -*- coding: utf-8 -*-
from atlantis import core
from loggingd import log_enter, log_return
from mqueue import cron, MINUTELY

@cron(MINUTELY)
def run():
    _update_sensors()
    _update_solution_statuses()
    problems = _update_problems()
    for problem in problems:
        _apply_solutions(problem)

@log_enter('Updating sensors ...')
def _update_sensors():
    for dev in core.devices.values():
        for sensor in dev.sensors():
            if sensor.should_update():
                sensor.update()
            
@log_enter('Updating solution statuses ...')
def _update_solution_statuses():
    for dev in core.devices.values():
        for solution in dev.solutions():
            solution.update()
        
@log_enter('Checking problems ...')
def _update_problems():
    problems = []
    for dev in core.devices.values():
        for problem in dev.problems():
            if problem.update():
                problems.append(problem)
    problems.sort(key=lambda p: (p.priority, p.name))
    return problems
    
@log_enter('Solving problem {problem.name()} ...')
def _apply_solutions(problem):
    solutions = _find_solutions(problem)
    while len(solutions) > 0:
        best = _find_best_solution(solutions)
        if best is None:
            break
        best.apply()
        solutions.remove(best)
        
def _find_solutions(problem):
    pname = problem.full_name()
    solutions = []
    for dev in core.devices.values():
        for solution in dev.solutions():
            if solution.problem == pname:
                solutions.append(solution)
    return solutions
    
@log_return('Found solution {ret.name()}.', condition='ret is not None')
def _find_best_solution(solutions):
    fitnesses = {s: s.fitness() for s in solutions}
    fitnesses = fitnesses.items()
    fitnesses.sort(key=lambda item: -item[1])
    best, fitness = fitnesses[0]
    return best if fitness > 0 else None
    