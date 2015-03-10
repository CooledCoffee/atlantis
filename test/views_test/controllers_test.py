# -*- coding: utf-8 -*-
from atlantis.device import AbstractDevice, Controller
from atlantis.views import controllers
from testutil import TestCase

class TriggerTest(TestCase):
    def test(self):
        # set up
        class SpeakerDevice(AbstractDevice):
            @Controller('power')
            def on(self):
                TriggerTest.power = True
        
        controllers.trigger('speaker.on')
        self.assertTrue(self.power)
        