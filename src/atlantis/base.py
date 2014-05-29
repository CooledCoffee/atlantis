# -*- coding: utf-8 -*-

class SingletonType(type):
    def __init__(self, name, bases, attrs):
        super(SingletonType, self).__init__(name, bases, attrs)
        self._instance = None if self._is_abstract() else self()
        
class Singleton(object):
    __metaclass__ = SingletonType
    
    @classmethod
    def instance(cls):
        return cls._instance
    
    @classmethod
    def _is_abstract(cls):
        return cls.__name__.startswith('Abstract')

class AutoRegisterType(SingletonType):
    def __init__(self, name, bases, attrs):
        super(AutoRegisterType, self).__init__(name, bases, attrs)
        if not self._is_abstract():
            self._register()
    
class AbstractComponent(Singleton):
    __metaclass__ = AutoRegisterType
    
    @classmethod
    def _register(cls):
        raise NotImplementedError()
    