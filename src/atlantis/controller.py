# -*- coding: utf-8 -*-
from atlantis.base import AutoNameComponent
from loggingd import log_enter

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
    