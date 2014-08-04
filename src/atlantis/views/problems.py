# -*- coding: utf-8 -*-
from atlantis.db import ProblemModel
from decorated.base.context import ctx
from metaweb import api

@api
def enable(name, enabled):
    model = ctx.session.get_or_create(ProblemModel, name)
    model.disabled = not enabled
