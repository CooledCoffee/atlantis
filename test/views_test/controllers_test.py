# -*- coding: utf-8 -*-
from atlantis.device import AbstractDevice, Controller
from atlantis.views import controllers
from testutil import TestCase

class SpeakerDevice(AbstractDevice):
    @Controller('power')
    def on(self):
        SpeakerDevice.power = True

class TriggerTest(TestCase):
    def test(self):
        controllers.trigger('speaker.on')
        self.assertTrue(SpeakerDevice.power)
        