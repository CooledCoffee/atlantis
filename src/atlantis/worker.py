# -*- coding: utf-8 -*-
from atlantis import device, rule
from loggingd import log_enter, log_return
from mqueue import cron, MINUTELY

@cron(MINUTELY)
def run():
    _update_sensors()
    _update_solution_statuses()
    problems = _update_problems()
    for problem in problems:
        solution = _find_best_solution(problem)
        if solution is not None:
            solution.apply(problem)

@log_enter('Updating sensors ...')
def _update_sensors():
    for d in device.devices.values():
        for sensor in d.sensors:
            if sensor.should_update():
                sensor.update()
            
@log_enter('Updating solution statuses ...')
def _update_solution_statuses():
    for solution in rule.solutions.values():
        solution.update()
        
@log_enter('Checking problems ...')
def _update_problems():
    return [p for p in rule.problems.values() if p.update()]
    
@log_enter('Solving problem {problem.name} ...')
def _apply_solutions(problem):
    solutions = _find_solutions(problem)
    while len(solutions) > 0:
        best = _find_best_solution(problem, solutions)
        if best is None:
            break
        best.apply(problem)
        solutions.remove(best)
        
def _find_solutions(problem):
    problem_class = type(problem)
    return [s for s in rule.solutions.values() if problem_class in s.targets]
    
@log_return('Found solution {ret.name}.', condition='ret is not None')
def _find_best_solution(problem, solutions):
    fitnesses = {s: s.fitness(problem) for s in solutions}
    fitnesses = fitnesses.items()
    fitnesses.sort(key=lambda item: -item[1])
    best, fitness = fitnesses[0]
    return best if fitness > 0 else None
    