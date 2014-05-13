# -*- coding: utf-8 -*-
from fixtures2 import TestCase
from sqlalchemy_dao.testing import MysqlFixture
import os

class DbTestCase(TestCase):
    def setUp(self):
        super(DbTestCase, self).setUp()
        script = os.path.join(os.path.dirname(__file__), 'atlantis.sql')
        self.mysql = self.useFixture(MysqlFixture([script],
                daos=['atlantis.db.dao']))
        