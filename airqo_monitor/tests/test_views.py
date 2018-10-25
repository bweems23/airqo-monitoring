import collections
import mock

from datetime import datetime
from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase, RequestFactory

from airqo_monitor.models import (
    Channel,
    ChannelNote,
    Incident,
    IncidentMalfunctionReasonLink,
    MalfunctionReason,
)
from airqo_monitor.views import channel_detail


class TestChannelDetailView(TestCase):
    def setUp(self):
        pass

    @mock.patch('airqo_monitor.views.render')
    def test_create_incident(self, render_mocker):
        channel = Channel.objects.create(channel_id=1, name='Test Name')
        incident = Incident.objects.create(channel=channel)
        
        channel_detail({}, channel.id)

        render_mocker.assert_called_with(
            {},
            "channel_detail.html",
            context={
                "channel": {
                    "channel_id": channel.id,
                    "name": channel.name,
                },
                "incidents": [
                    collections.OrderedDict(
                        created_at=datetime.strftime(incident.created_at,'%Y-%m-%dT%H:%M:%S.%fZ'),
                        resolved_at=None,
                        malfunction_reasons=[],
                    )
                ]
            }
        )