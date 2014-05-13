# -*- coding: utf-8 -*-
from atlantis import util
from fixtures2 import TestCase

class ThermometerDevice(object):
    pass

class AirConditioningDevice(object):
    pass

class CalcNameTest(TestCase):
    def test_single_word(self):
        name = util.calc_name(ThermometerDevice)
        self.assertEqual('thermometer', name)
        
    def test_multi_words(self):
        name = util.calc_name(AirConditioningDevice)
        self.assertEqual('air_conditioning', name)
        