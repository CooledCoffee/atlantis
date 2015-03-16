# -*- coding: utf-8 -*-
from atlantis import core
from metaweb import api

@api
def trigger(name):
    controller = core.clocate(name)
    controller()
