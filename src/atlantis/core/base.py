# -*- coding: utf-8 -*-
from decorated import Function, ctx

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
    
class DeviceComponent(Function):
    model_type = None
    
    def full_name(self, device):
        return '%s.%s' % (type(device).name, self.__name__)
    
    def name(self, device):
        return self.__name__
    
    def _get_model(self, device, create=False):
        if create:
            return ctx.session.get_or_create(self.model_type, self.full_name(device))
        else:
            return ctx.session.get(self.model_type, self.full_name(device))
    
    def _get_model_field(self, device, field, default=False):
        model = self._get_model(device)
        return getattr(model, field) if model is not None else default
    
class ExpiredError(Exception):
    pass
    