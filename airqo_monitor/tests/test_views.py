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

        actual_calls = render_mocker.call_args_list
        assert len(actual_calls) == 1
        call = actual_calls[0]
        assert call[0] == ({}, 'channel_detail.html')
        call_context = call[1]['context']

        channel_data = call_context['channel']
        assert channel_data['channel_id'] == self.channel.id
        assert channel_data['name'] == self.channel.name
        len(channel_data['active_incidents']) == 1
        assert channel_data['active_incidents'][0] == collections.OrderedDict(
            created_at=datetime.strftime(incident.created_at,'%Y-%m-%dT%H:%M:%S.%fZ'),
            resolved_at=None,
            malfunction_reason=collections.OrderedDict(
                name=self.malfunction_reason.name,
                description=self.malfunction_reason.description,
            ),
        )

        history_data = call_context['history']
        assert len(history_data) == 1
        assert history_data[0]['object_type'] == 'incident'
        assert history_data[0]['created_at'] == datetime.strftime(incident.local_created_at,'%d/%m/%Y at %H:%M')
        assert history_data[0]['note'] == None
        assert history_data[0]['author'] == None
        assert history_data[0]['resolved_at'] == None
        assert history_data[0]['malfunction_reason'] == {
            "name": self.malfunction_reason.name,
            "description": self.malfunction_reason.description,
        }


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
