# -*- coding: utf-8 -*-
from atlantis.views import controllers
from fixtures._fixtures.monkeypatch import MonkeyPatch
from fixtures2 import TestCase, MoxFixture

class TriggerTest(TestCase):
    def test(self):
        # set up
        self.mox = self.useFixture(MoxFixture())
        speaker = self.mox.create_mock()
        self.useFixture(MonkeyPatch('atlantis.device.devices', {'speaker': speaker}))
        
        # test
        with self.mox.record():
            speaker.on()
        with self.mox.replay():
            controllers.trigger('speaker.on')
            