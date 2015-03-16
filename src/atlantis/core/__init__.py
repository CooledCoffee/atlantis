# -*- coding: utf-8 -*-

devices = {}

def clocate(full_name):
    dname, cname = full_name.split('.')
    device = devices.get(dname)
    return getattr(device, cname)
