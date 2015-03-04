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
        
    def controllers(self):
        return self._list_components(Controller)
    
    def sensors(self):
        return self._list_components(Sensor)
    
    def _list_components(self, type):
        results = []
        for attr in dir(self):
            method = getattr(self, attr)
            if not hasattr(method, 'im_func'):
                continue
            if isinstance(method.im_func, type):
                results.append(method)
        return results

class AutoNameComponent(Function):
    def full_name(self, device):
        return '%s.%s' % (type(device).name, self.__name__)
    
    def name(self, device):
        return self.__name__
    
class Sensor(AutoNameComponent):
    def available(self, device):
        if self.interval is None:
            return True
        elapsed = (datetime.now() - self.time(device)).total_seconds()
        threshold = 2.5 * self.interval
        return elapsed < threshold
     
    def should_update(self, device):
        if self.interval is None:
            return False
        elapsed = (datetime.now() - self.time(device)).total_seconds()
        return elapsed > self.interval - 10
    
    def time(self, device):
        sensor = self._get_model(device)
        return sensor.time if sensor is not None else datetime(1970, 1, 1)
    
    @log_enter('Updating sensor {self.full_name} ...')
    @log_and_ignore_error('Failed to update sensor {self.full_name}.', exc_info=True)
    def update(self, device):
        try:
            value = self._call(device)
            self.value(device, value)
            sensor = self._get_model(device)
            sensor.error_rate = _calc_error_rate(sensor.error_rate, self.interval, False)
        except:
            sensor = self._get_model(device, create=True)
            sensor.error_rate = _calc_error_rate(sensor.error_rate, self.interval, True)
            raise
    
    def value(self, device, value=None):
        if value is None:
            if not self.available(device):
                raise ExpiredError('Sensor %s has expired.' % self.full_name(device))
            model = self._get_model(device)
            return json.loads(model.value) if model is not None else None
        else:
            model = self._get_model(device, create=True)
            model.value = json.dumps(value)
            model.time = datetime.now()
    
    def _get_model(self, device, create=False):
        if create:
            return ctx.session.get_or_create(SensorModel, self.full_name(device))
        else:
            return ctx.session.get(SensorModel, self.full_name(device))
     
    def _init(self, interval=60):
        super(Sensor, self)._init()
        self.interval = interval
        self._device = None
        
    def _retrieve(self):
        raise NotImplementedError()
    
class Controller(AutoNameComponent):
    def _init(self, group, order=0, invalidates=None):
        super(Controller, self)._init()
        self.group = group
        self.order = order
        self._invalidates = invalidates
        
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
    