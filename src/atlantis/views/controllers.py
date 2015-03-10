# -*- coding: utf-8 -*-
from atlantis import device
from metaweb import api

@api
def trigger(name):
    controller = device.locate_comp(name)
    controller()
