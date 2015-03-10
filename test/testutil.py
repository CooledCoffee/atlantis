# -*- coding: utf-8 -*-
from fixtures2 import TestCase, PatchesFixture, MoxFixture
from sqlalchemy_dao.testing import MysqlFixture
import os

class TestCase(TestCase):
    def setUp(self):
        super(TestCase, self).setUp()
        self.patches = self.useFixture(PatchesFixture())
        self.mox = self.useFixture(MoxFixture())
        self.patches.patch('atlantis.device.devices', {})

class DbTestCase(TestCase):
    def setUp(self):
        super(DbTestCase, self).setUp()
        script = os.path.join(os.path.dirname(__file__), 'atlantis.sql')
        self.mysql = self.useFixture(MysqlFixture([script],
                daos=['atlantis.db.dao']))
        