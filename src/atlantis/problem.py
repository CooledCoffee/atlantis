# -*- coding: utf-8 -*-
from atlantis import db
from atlantis.base import DeviceComponent
from atlantis.db import ProblemModel
from decorated import ctx
from loggingd import log_enter, log_return, log_and_ignore_error

class Problem(DeviceComponent):
    def enabled(self, device):
        return not self._get_bool_field(device, 'disabled')
        
    def exists(self, device):
        return self._get_bool_field(device, 'exists')
    
    @log_enter('[DEBUG] Updating problem {self.name} ...')
    @log_return('Found problem {self.name}.', condition='ret')
    @log_and_ignore_error('Failed to update problem {self.name}.', exc_info=True)
    def update(self, device):
        if not self.enabled(device):
            return False
        exists = self._call(device)
        model = self._get_model(device, create=True)
        model.exists = exists
        return exists
    
    def _init(self, priority=0, description=''):
        super(Problem, self)._init()
        self.description = description
        self.priority = priority
    