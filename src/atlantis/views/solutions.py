# -*- coding: utf-8 -*-
from atlantis.db import SolutionModel
from decorated.base.context import ctx
from metaweb import api

@api
def enable(name, problem, enabled):
    model = ctx.session.get_or_create(SolutionModel, name)
    problems = model.disabled.split(',') if model.disabled is not None else []
    if enabled:
        problems.remove(problem)
    else:
        problems.append(problem)
    model.disabled = ','.join(problems)
