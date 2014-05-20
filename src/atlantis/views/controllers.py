# -*- coding: utf-8 -*-
from atlantis import device
from metaweb import api

@api
def trigger(name):
    dname, cname = name.rsplit('.')
    dev = device.devices[dname]
    controller = getattr(dev, cname)
    controller()
