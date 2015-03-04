# -*- coding: utf-8 -*-
from atlantis import db
from atlantis.db import ProblemModel
from testutil import DbTestCase

class ExistsTest(DbTestCase):
    def test_true(self):
        # set up
        with self.mysql.dao.create_session() as session:
            session.add(ProblemModel(name='thermometer.too_high', exists=True))
            
        # test
        with self.mysql.dao.SessionContext():
            result = db.get_bool_field(ProblemModel, 'thermometer.too_high', 'exists')
            self.assertTrue(result)
            
    def test_false(self):
        # set up
        with self.mysql.dao.create_session() as session:
            session.add(ProblemModel(name='thermometer.too_high', exists=False))
            
        # test
        with self.mysql.dao.SessionContext():
            result = db.get_bool_field(ProblemModel, 'thermometer.too_high', 'exists')
            self.assertFalse(result)
            
    def test_no_record(self):
        # test
        with self.mysql.dao.SessionContext():
            result = db.get_bool_field(ProblemModel, 'thermometer.too_high', 'exists')
            self.assertFalse(result)
            