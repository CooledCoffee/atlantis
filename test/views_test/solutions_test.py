# -*- coding: utf-8 -*-
from atlantis.db import SolutionModel
from atlantis.views import solutions
from testutil import DbTestCase

class EnableTest(DbTestCase):
    def test_enable(self):
        # set up
        with self.mysql.dao.create_session() as session:
            session.add(SolutionModel(name='window.open_for_cooling', enabled=False))
        
        # test
        with self.mysql.dao.SessionContext():
            solutions.enable('window.open_for_cooling', True)
            
        # verify
        with self.mysql.dao.create_session() as session:
            model = session.get(SolutionModel, 'window.open_for_cooling')
            self.assertTrue(model.enabled)
            
    def test_disable(self):
        # set up
        with self.mysql.dao.create_session() as session:
            session.add(SolutionModel(name='window.open_for_cooling', enabled=True))
        
        # test
        with self.mysql.dao.SessionContext():
            solutions.enable('window.open_for_cooling', False)
            
        # verify
        with self.mysql.dao.create_session() as session:
            model = session.get(SolutionModel, 'window.open_for_cooling')
            self.assertFalse(model.enabled)
            