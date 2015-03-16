# -*- coding: utf-8 -*-
from atlantis import util
from atlantis.core.base import AbstractComponent
from atlantis.core.controller import Controller
from atlantis.core.problem import Problem
from atlantis.core.sensor import Sensor
from atlantis.core.solution import Solution

class AbstractDevice(AbstractComponent):
    @classmethod
    def _register(cls):
        from atlantis import core
        cls.name = util.calc_name(cls)
        device = cls.instance()
        core.devices[cls.name] = device
        
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
