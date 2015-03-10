# -*- coding: utf-8 -*-
from atlantis.db import ProblemModel
from atlantis.views import problems
from testutil import DbTestCase

class EnableTest(DbTestCase):
    def test_enable(self):
        with self.mysql.dao.SessionContext():
            problems.enable('thermometer.too_high', True)
        with self.mysql.dao.create_session() as session:
            model = session.get(ProblemModel, 'thermometer.too_high')
            self.assertTrue(model.enabled)
            
    def test_disable(self):
        with self.mysql.dao.SessionContext():
            problems.enable('thermometer.too_high', False)
        with self.mysql.dao.create_session() as session:
            model = session.get(ProblemModel, 'thermometer.too_high')
            self.assertFalse(model.enabled)
            