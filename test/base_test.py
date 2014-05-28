# -*- coding: utf-8 -*-
from atlantis.base import Singleton, AutoRegisterComponent
from testutil import TestCase

class SingletonTypeTest(TestCase):
    def test(self):
        class TestType(Singleton):
            pass
        self.assertIsInstance(TestType.instance(), TestType)

class AutoRegisterTypeTest(TestCase):
    def test(self):
        AutoRegisterTypeTest.classes = []
        class TestType(AutoRegisterComponent):
            @classmethod
            def _register(cls):
                AutoRegisterTypeTest.classes.append(cls)
        class Foo(TestType):
            pass
        class Bar(TestType):
            pass
        self.assertEqual([Foo, Bar], self.classes)
        