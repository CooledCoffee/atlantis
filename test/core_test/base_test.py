# -*- coding: utf-8 -*-
from atlantis.core.base import Singleton, AbstractComponent
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
        class AbstractDevice(AbstractComponent):
            @classmethod
            def _register(cls):
                AbstractComponentTest.classes.append(cls)
        class FooDevice(AbstractDevice):
            pass
        class BarDevice(AbstractDevice):
            pass
        self.assertEqual([FooDevice, BarDevice], self.classes)
        