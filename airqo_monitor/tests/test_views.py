import collections
import mock

from bunch import Bunch
from datetime import datetime
from django.test import TestCase

from airqo_monitor.models import (
    Channel,
    ChannelNote,
    Incident,
)
from airqo_monitor.views import (
    channel_detail,
    channel_notes,
)


class TestChannelDetailView(TestCase):
    def setUp(self):
        self.channel = Channel.objects.create(channel_id=1, name='Test Name')

    @mock.patch('airqo_monitor.views.render')
    def test_create_incident(self, render_mocker):
        incident = Incident.objects.create(channel=self.channel)
        
        channel_detail({}, self.channel.id)

        render_mocker.assert_called_once_with(
            {},
            "channel_detail.html",
            context={
                "channel": {
                    "channel_id": self.channel.id,
                    "name": self.channel.name,
                },
                "history": [
                    collections.OrderedDict(
                        object_type='incident',
                        created_at=datetime.strftime(incident.created_at,'%Y-%m-%dT%H:%M:%S.%fZ'),
                        note=None,
                        author=None,
                        resolved_at=None,
                        malfunction_reasons=[],
                    )
                ]
            }
        )

    @mock.patch('airqo_monitor.views.redirect')
    def test_channel_notes(self, redirect_mocker):
        request = Bunch(
            method='POST',
            POST={
                'channel': self.channel.channel_id,
                'note': 'notenote',
                'author': 'rachel',
            }
        )
        channel_notes(request)
        redirect_mocker.assert_called_once_with(
            '/channels/{}/'.format(self.channel.channel_id)
        )

        note = ChannelNote.objects.last()
        assert note.channel == self.channel
        assert note.author == 'rachel'
        assert note.note == 'notenote'
