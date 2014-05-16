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
                obj.full_name = '%s.%s' % (cls.name, obj.name)
                obj._device = device
                cls.sensors.append(attr)
            elif hasattr(obj, 'im_func') and isinstance(obj.im_func, Controller):
                c = obj.im_func
                c.name = attr
                c.full_name = '%s.%s' % (cls.name, c.name)
                c._device = device
                cls.controllers.append(attr)
    
class Sensor(object):
    def __init__(self, interval=60):
        self.name = None
        self.full_name = None
        self._device = None
        self._interval = interval
        
    @property
    def time(self):
        sensor = ctx.session.get(SensorModel, self.full_name)
        return sensor.time if sensor is not None else datetime(1970, 1, 1)
    
    @property
    def value(self):
        sensor = ctx.session.get(SensorModel, self.full_name)
        return json.loads(sensor.value) if sensor is not None else None
    
    @value.setter
    def value(self, value):
        sensor = ctx.session.get_or_create(SensorModel, self.full_name)
        sensor.value = json.dumps(value)
        sensor.time = datetime.now()
        
    def available(self):
        ellapsed = (datetime.now() - self.time).total_seconds()
        threshold = 2.5 * self._interval
        return ellapsed < threshold
    
    @log_enter('Updating sensor {self.full_name} ...')
    @log_and_ignore_error('Failed to update sensor {self.full_name}.')
    def update(self, force=False):
        elapsed = (datetime.now() - self.time).total_seconds()
        if force or elapsed > self._interval - 10:
            self.value = self._retrieve()
    
    def _retrieve(self):
        raise NotImplementedError()

class Controller(Function):
    def _init(self, affects=None):
        super(Controller, self)._init()
        self._affects = affects
        self.name = None
        self.full_name = None
        self._device = None
        
    @log_enter('Triggering controller {self.full_name} ...')
    def _call(self, *args, **kw):
        result = super(Controller, self)._call(*args, **kw)
        if self._affects:
            prop = getattr(self._device, self._affects)
            prop.update()
        return result
    