# -*- coding: utf-8 -*-
from atlantis.base import AutoRegisterType
from fixtures2 import TestCase

class AutoRegisterTypeTest(TestCase):
    def test(self):
        self.classes = []
        case = self
        class TestType(object):
            __metaclass__ = AutoRegisterType
            @classmethod
            def _register(cls):
                case.classes.append(cls)
        class Foo(TestType):
            pass
        class Bar(TestType):
            pass
        self.assertEqual([Foo, Bar], self.classes)
        