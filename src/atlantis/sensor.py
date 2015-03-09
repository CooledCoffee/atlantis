# -*- coding: utf-8 -*-
from atlantis.base import DeviceComponent, ExpiredError
from atlantis.db import SensorModel
from datetime import datetime
from decorated import ctx
from loggingd import log_enter, log_and_ignore_error
import doctest
import json

class Sensor(DeviceComponent):
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
     
    def _init(self, interval=60):
        super(Sensor, self)._init()
        self.interval = interval
        self._device = None
        
    def _retrieve(self):
        raise NotImplementedError()
    
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
    