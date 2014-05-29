# -*- coding: utf-8 -*-
from atlantis.base import Singleton, AbstractComponent
from testutil import TestCase

class SingletonTest(TestCase):
    def test_normal(self):
        class TestSingleton(Singleton):
            pass
        self.assertIsInstance(TestSingleton.instance(), TestSingleton)
        
    def test_abstract(self):
        class AbstractSingleton(Singleton):
            pass
        self.assertIsNone(AbstractComponent.instance())

class AbstractComponentTest(TestCase):
    def test(self):
        AbstractComponentTest.classes = []
        class TestType(AbstractComponent):
            @classmethod
            def _register(cls):
                AbstractComponentTest.classes.append(cls)
        class Foo(TestType):
            pass
        class Bar(TestType):
            pass
        self.assertEqual([Foo, Bar], self.classes)
        