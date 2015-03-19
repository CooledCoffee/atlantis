# -*- coding: utf-8 -*-
from atlantis.core.base import DeviceComponent
from loggingd import log_enter

class Controller(DeviceComponent):
    def _init(self, group, order=0, invalidate=None):
        super(Controller, self)._init()
        self.group = group
        self.order = order
        self._invalidate = invalidate
        
    @log_enter('Triggering controller {self.full_name()} ...')
    def trigger(self, device):
        result = self._call(device)
        if self._invalidate is not None:
            sensor = getattr(device, self._invalidate)
            sensor.update()
        return result
    