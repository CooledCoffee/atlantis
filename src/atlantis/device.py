# -*- coding: utf-8 -*-
from atlantis import util
from atlantis.base import AutoRegisterType
from atlantis.db import SensorModel
from datetime import datetime
from decorated import Function
from decorated.base.context import ctx
from loggingd import log_and_ignore_error, log_enter
import json

devices = {}

class Device(object):
    __metaclass__ = AutoRegisterType
    
    @classmethod
    def _register(cls):
        cls.name = util.calc_name(cls)
        device = cls()
        devices[cls.name] = device
        cls.sensors = []
        cls.controllers = []
        for attr in dir(device):
            obj = getattr(device, attr)
            if isinstance(obj, Sensor):
                obj.name = attr
                obj._device = device
                cls.sensors.append(attr)
            elif hasattr(obj, 'im_func') and isinstance(obj.im_func, controller):
                obj.im_func._device = device
                cls.controllers.append(attr)
    
class Sensor(object):
    def __init__(self, interval=60):
        self.name = None
        self._device = None
        self._interval = interval
        
    @property
    def full_name(self):
        return '%s.%s' % (self._device.name, self.name) 
        
    @property
    def time(self):
        sensor = ctx.session.get(SensorModel, self.full_name)
        return sensor.time if sensor is not None else datetime(2000, 1, 1)
    
    @property
    def value(self):
        sensor = ctx.session.get(SensorModel, self.full_name)
        return json.loads(sensor.value) if sensor is not None else None
    
    @value.setter
    def value(self, value):
        sensor = ctx.session.get_or_create(SensorModel, self.full_name)
        sensor.value = json.dumps(value)
        sensor.time = datetime.now()
        
    @log_enter('Updating sensor {self.full_name} ...')
    @log_and_ignore_error('Failed to update sensor {self.full_name}.')
    def update(self, force=False):
        elapsed = (datetime.now() - self.time).total_seconds()
        if force or elapsed > self._interval:
            self.value = self._retrieve()
    
    def _retrieve(self):
        raise NotImplementedError()

class controller(Function):
    def _init(self, affects=None):
        super(controller, self)._init()
        self._affects = affects
        
    def _call(self, *args, **kw):
        result = super(controller, self)._call(*args, **kw)
        if self._affects:
            prop = getattr(self._device, self._affects)
            prop.update()
        return result
    