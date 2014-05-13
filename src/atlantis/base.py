# -*- coding: utf-8 -*-

class AutoRegisterType(type):
    def __init__(self, name, bases, dict):
        super(AutoRegisterType, self).__init__(name, bases, dict)
        if '_register' not in self.__dict__:
            self._register()
    
    @classmethod
    def _register(cls):
        raise NotImplementedError()
    