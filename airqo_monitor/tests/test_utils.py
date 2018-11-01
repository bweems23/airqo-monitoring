import collections
import mock

from datetime import datetime
from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase, RequestFactory

from airqo_monitor.models import (
    Channel,
    ChannelNote,
    Incident,
    MalfunctionReason,
)
from airqo_monitor.utils import (
    create_channel_note,
    get_channel_history,
)


class TestUtils(TestCase):
    def setUp(self):
        self.channel = Channel.objects.create(channel_id=1, name='Test Name')

    def test_get_channel_history(self):
        note1 = ChannelNote.objects.create(
            channel=self.channel,
            author='Rachel',
            note='note',
        )
        note2 = ChannelNote.objects.create(
            channel=self.channel,
            author='Rachel',
            note='note',
        )
        incident1 = Incident.objects.create(
            channel=self.channel
        )
        note3 = ChannelNote.objects.create(
            channel=self.channel,
            author='Rachel',
            note='note',
        )
        incident2 = Incident.objects.create(
            channel=self.channel
        )
        history = get_channel_history(self.channel)
        assert history[0] == incident2
        assert history[1] == note3
        assert history[2] == incident1
        assert history[3] == note2
        assert history[4] == note1

    def test_create_channel_note(self):
        note = create_channel_note(self.channel.channel_id, 'Rachel', 'note')
        assert note.note == 'note'
        assert note.author == 'Rachel'
        assert note.channel == self.channel
