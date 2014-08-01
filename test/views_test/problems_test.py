# -*- coding: utf-8 -*-
from atlantis.db import ProblemModel
from atlantis.views import problems
from testutil import DbTestCase

class EnableTest(DbTestCase):
    def test_enable(self):
        with self.mysql.dao.SessionContext():
            problems.enable('TEMPERATURE_TOO_HIGH', True)
        with self.mysql.dao.create_session() as session:
            model = session.get(ProblemModel, 'TEMPERATURE_TOO_HIGH')
            self.assertTrue(model.enabled)
            
    def test_disable(self):
        with self.mysql.dao.SessionContext():
            problems.enable('TEMPERATURE_TOO_HIGH', False)
        with self.mysql.dao.create_session() as session:
            model = session.get(ProblemModel, 'TEMPERATURE_TOO_HIGH')
            self.assertFalse(model.enabled)
            