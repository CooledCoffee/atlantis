# -*- coding: utf-8 -*-
from atlantis.views import controllers
from testutil import TestCase

class TriggerTest(TestCase):
    def test(self):
        # set up
        speaker = self.mox.create_mock()
        self.patches.patch('atlantis.device.devices', {'speaker': speaker})
        
        # test
        with self.mox.record():
            speaker.on()
        with self.mox.replay():
            controllers.trigger('speaker.on')
            