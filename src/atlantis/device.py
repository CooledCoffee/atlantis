# -*- coding: utf-8 -*-
from atlantis import util
from atlantis.base import AbstractComponent
from atlantis.controller import Controller
from atlantis.problem import Problem
from atlantis.sensor import Sensor
from atlantis.solution import Solution

devices = {}

class AbstractDevice(AbstractComponent):
    @classmethod
    def _register(cls):
        cls.name = util.calc_name(cls)
        device = cls.instance()
        devices[cls.name] = device
        
    def controllers(self):
        return self._list_components(Controller)
    
    def problems(self):
        return self._list_components(Problem)
    
    def sensors(self):
        return self._list_components(Sensor)
    
    def solutions(self):
        return self._list_components(Solution)
    
    def _list_components(self, component_type):
        results = []
        for attr in dir(self):
            method = getattr(self, attr)
            if not hasattr(method, 'im_func'):
                continue
            if isinstance(method.im_func, component_type):
                results.append(method)
        return results

def locate_comp(full_name):
    dname, cname = full_name.split('.')
    device = devices.get(dname)
    return getattr(device, cname)
