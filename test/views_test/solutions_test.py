# -*- coding: utf-8 -*-
from atlantis.db import SolutionModel
from atlantis.views import solutions
from testutil import DbTestCase

class EnableTest(DbTestCase):
    def test_enable(self):
        # set up
        with self.mysql.dao.create_session() as session:
            session.add(SolutionModel(name='OPEN_WINDOW', disabled='TEMPERATURE_TOO_HIGH'))
        
        # test
        with self.mysql.dao.SessionContext():
            solutions.enable('OPEN_WINDOW', 'TEMPERATURE_TOO_HIGH', True)
            
        # verify
        with self.mysql.dao.create_session() as session:
            model = session.get(SolutionModel, 'OPEN_WINDOW')
            self.assertEqual('', model.disabled)
            
    def test_disable(self):
        with self.mysql.dao.SessionContext():
            solutions.enable('OPEN_WINDOW', 'TEMPERATURE_TOO_HIGH', False)
        with self.mysql.dao.create_session() as session:
            model = session.get(SolutionModel, 'OPEN_WINDOW')
            self.assertEqual('TEMPERATURE_TOO_HIGH', model.disabled)
            