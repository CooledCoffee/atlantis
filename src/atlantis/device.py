# -*- coding: utf-8 -*-
from atlantis import util
from atlantis.base import AbstractComponent, ExpiredError
from atlantis.db import SensorModel
from datetime import datetime
from decorated import Function
from decorated.base.context import ctx
from loggingd import log_and_ignore_error, log_enter
import doctest
import json

devices = {}

class AbstractDevice(AbstractComponent):
    @classmethod
    def _register(cls):
        cls.name = util.calc_name(cls)
        device = cls.instance()
        devices[cls.name] = device
        cls.sensors = []
        cls.controllers = []
        for attr in dir(device):
            obj = getattr(device, attr)
            if isinstance(obj, Sensor):
                obj.name = attr
                obj.full_name = '%s.%s' % (cls.name, obj.name)
                obj._device = device
                cls.sensors.append(obj)
            elif hasattr(obj, 'im_func') and isinstance(obj.im_func, Controller):
                c = obj.im_func
                c.name = attr
                c.full_name = '%s.%s' % (cls.name, c.name)
                c._device = device
                cls.controllers.append(obj)
    
class Sensor(object):
    def __init__(self, interval=60):
        self.name = None
        self.full_name = None
        self.interval = interval
        self._device = None
        self._last_update_time = datetime(1970, 1, 1)
        
    @property
    def time(self):
        sensor = self._get_model()
        return sensor.time if sensor is not None else datetime(1970, 1, 1)
    
    @property
    def value(self):
        if not self.available():
            raise ExpiredError('Sensor %s has expired.' % self.full_name)
        sensor = self._get_model()
        return json.loads(sensor.value) if sensor is not None else None
    
    @value.setter
    def value(self, value):
        sensor = self._get_model(create=True)
        sensor.value = json.dumps(value)
        sensor.time = datetime.now()
        
    def available(self):
        if self.interval is None:
            return True
        elapsed = (datetime.now() - self.time).total_seconds()
        threshold = 2.5 * self.interval
        return elapsed < threshold
    
    def should_update(self):
        if self.interval is None:
            return False
        elapsed = (datetime.now() - self._last_update_time).total_seconds()
        return elapsed > self.interval - 10

    @log_enter('Updating sensor {self.full_name} ...')
    @log_and_ignore_error('Failed to update sensor {self.full_name}.', exc_info=True)
    def update(self):
        try:
            self.value = self._retrieve()
            sensor = self._get_model()
            sensor.error_rate = _calc_error_rate(sensor.error_rate, self.interval, False)
        except:
            sensor = self._get_model(create=True)
            sensor.error_rate = _calc_error_rate(sensor.error_rate, self.interval, True)
        self._last_update_time = datetime.now()
    
    def _get_model(self, create=False):
        if create:
            return ctx.session.get_or_create(SensorModel, self.full_name)
        else:
            return ctx.session.get(SensorModel, self.full_name)
    
    def _retrieve(self):
        raise NotImplementedError()
    
class Controller(Function):
    def _init(self, group, order=0, invalidates=None):
        super(Controller, self)._init()
        self.group = group
        self.order = order
        self._invalidates = invalidates
        self.name = None
        self.full_name = None
        self._device = None
        
    @log_enter('Triggering controller {self.full_name} ...')
    def trigger(self, device):
        result = self._call(device)
        if self._invalidates is not None:
            prop = getattr(device, self._invalidates)
            prop.update()
        return result
    
def _calc_error_rate(rate, interval, error):
    '''
    >>> _calc_error_rate(0.1, 60, True)
    0.10064632080671107
    >>> _calc_error_rate(0.1, 60, False)
    0.09995187636226663
    >>> _calc_error_rate(None, 60, True)
    0.0006944444444444445
    >>> _calc_error_rate(None, 60, False)
    0.0
    '''
    if rate is None:
        rate = 0
    times_per_day = 86400 / interval
    decay_ratio = 0.5 ** (1.0 / times_per_day)
    rate *= decay_ratio
    if error:
        rate += 1.0 / times_per_day
    return rate

if __name__ == '__main__':
    doctest.testmod()
    