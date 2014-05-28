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
        self.classes = []
        case = self
        class TestType(AutoRegisterComponent):
            @classmethod
            def _register(cls):
                case.classes.append(cls)
        class Foo(TestType):
            pass
        class Bar(TestType):
            pass
        self.assertEqual([Foo, Bar], self.classes)
        