# -*- coding: utf-8 -*-
from atlantis import db
from atlantis.base import AutoNameComponent
from atlantis.db import ProblemModel
from decorated import ctx
from loggingd import log_enter, log_return, log_and_ignore_error

class Problem(AutoNameComponent):
    def enabled(self, device):
        name = self.full_name(device)
        return not db.get_bool_field(ProblemModel, name, 'disabled',
                default=False)
        
    def exists(self, device):
        name = self.full_name(device)
        return db.get_bool_field(ProblemModel, name, 'exists')
    
    @log_enter('[DEBUG] Updating problem {self.name} ...')
    @log_return('Found problem {self.name}.', condition='ret')
    @log_and_ignore_error('Failed to update problem {self.name}.', exc_info=True)
    def update(self, device):
        if not self.enabled(device):
            return False
        exists = self._call(device)
        name = self.full_name(device)
        model = ctx.session.get_or_create(ProblemModel, name)
        model.exists = exists
        return exists
    
    def _init(self, priority=0, description=''):
        super(Problem, self)._init()
        self.description = description
        self.priority = priority
    