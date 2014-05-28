# -*- coding: utf-8 -*-

class SingletonType(type):
    def __init__(self, name, bases, attrs):
        super(SingletonType, self).__init__(name, bases, attrs)
        self._instance = self()
        
class Singleton(object):
    __metaclass__ = SingletonType
    
    @classmethod
    def instance(cls):
        return cls._instance

class AutoRegisterType(SingletonType):
    def __init__(self, name, bases, attrs):
        super(AutoRegisterType, self).__init__(name, bases, attrs)
        if '_register' not in self.__dict__:
            self._register()
    
class AutoRegisterComponent(Singleton):
    __metaclass__ = AutoRegisterType
    
    @classmethod
    def _register(cls):
        raise NotImplementedError()
    