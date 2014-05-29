# -*- coding: utf-8 -*-
from atlantis import rule
from atlantis.db import ProblemModel
from testutil import DbTestCase

class ExistsTest(DbTestCase):
    def test_true(self):
        # set up
        with self.mysql.dao.create_session() as session:
            session.add(ProblemModel(name='TEMPERATURE_TOO_HIGH', exists=True))
            
        # test
        with self.mysql.dao.SessionContext():
            result = rule._get_bool_field(ProblemModel, 'TEMPERATURE_TOO_HIGH', 'exists')
            self.assertTrue(result)
            
    def test_false(self):
        # set up
        with self.mysql.dao.create_session() as session:
            session.add(ProblemModel(name='TEMPERATURE_TOO_HIGH', exists=False))
            
        # test
        with self.mysql.dao.SessionContext():
            result = rule._get_bool_field(ProblemModel, 'TEMPERATURE_TOO_HIGH', 'exists')
            self.assertFalse(result)
            
    def test_no_record(self):
        # test
        with self.mysql.dao.SessionContext():
            result = rule._get_bool_field(ProblemModel, 'TEMPERATURE_TOO_HIGH', 'exists')
            self.assertFalse(result)
            