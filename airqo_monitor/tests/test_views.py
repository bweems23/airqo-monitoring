import json
import collections
import mock

from bunch import Bunch
from datetime import datetime
from django.test import TestCase

from airqo_monitor.models import (
    Channel,
    ChannelNote,
    ChannelType,
    Incident,
    MalfunctionReason,
)
from airqo_monitor.views import (
    channel_detail,
    channel_notes,
)


class TestChannelDetailView(TestCase):
    def setUp(self):
        self.channel_type, _ = ChannelType.objects.get_or_create(name='airqo', data_format_json=json.dumps({}))
        self.channel = Channel.objects.create(channel_id=1, name='Test Name', channel_type=self.channel_type)
        self.malfunction_reason = MalfunctionReason.objects.create(name="Test Reason", description="test")

    @mock.patch('airqo_monitor.views.render')
    def test_create_incident(self, render_mocker):
        incident = Incident.objects.create(channel=self.channel, malfunction_reason=self.malfunction_reason)

        channel_detail({}, self.channel.id)

        render_mocker.assert_called_once_with(
            {},
            "channel_detail.html",
            context={
                "channel": {
                    "channel_id": self.channel.id,
                    "name": self.channel.name,
                    "active_incidents": [
                        collections.OrderedDict(
                            created_at=datetime.strftime(incident.created_at,'%Y-%m-%dT%H:%M:%S.%fZ'),
                            resolved_at=None,
                            malfunction_reason=collections.OrderedDict(
                                name=self.malfunction_reason.name,
                                description=self.malfunction_reason.description,
                            ),
                        )
                    ]
                },
                "history": [
                    collections.OrderedDict(
                        object_type='incident',
                        created_at=datetime.strftime(incident.local_created_at,'%d/%m/%Y at %H:%M'),
                        note=None,
                        author=None,
                        resolved_at=None,
                        malfunction_reason={
                            "name": self.malfunction_reason.name,
                            "description": self.malfunction_reason.description,
                        }
                    )
                ],
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
