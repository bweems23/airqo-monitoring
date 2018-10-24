from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase, RequestFactory

from airqo_monitor.models import (
    ChannelNote,
    Incident,
    IncidentMalfunctionReasonLink,
    MalfunctionReason,
)
from airqo_monitor.views import index


class TestIncidentModel(TestCase):
    def setUp(self):
        pass

    def test_create_incident(self):
        incident = Incident.objects.create(channel_id=1)
        assert incident.channel_id == 1
        assert incident.created_at is not None


class TestMalfunctionReasonModel(TestCase):
    def setUp(self):
        pass

    def test_create_malfunction_reason(self):
        reason = MalfunctionReason.objects.create(
            name='no_data',
            description="We didn't get any data back for the channel"
        )
        assert reason.name == 'no_data'
        assert reason.description == "We didn't get any data back for the channel"


class TestIncidentMalfunctionReasonLink(TestCase):
    def setUp(self):
        self.reason = MalfunctionReason.objects.create(
            name='no_data',
            description="We didn't get any data back for the channel"
        )
        self.incident = Incident.objects.create(channel_id=1)

    def test_link_reason_and_incident(self):
        IncidentMalfunctionReasonLink.objects.create(
            malfunction_reason=self.reason,
            incident=self.incident,
        )
        assert len(self.reason.incidents) == 1
        assert self.reason.incidents[0] == self.incident
        assert len(self.incident.malfunction_reasons) == 1
        assert self.incident.malfunction_reasons[0] == self.reason


class TestChannelNote(TestCase):
    def setUp(self):
        pass

    def test_create_channel_note(self):
        note = ChannelNote.objects.create(
            channel_id=1,
            note='did some maintenance',
            author='Rachel',
        )

        assert note.channel_id == 1
        assert note.note == 'did some maintenance'
        assert note.author == 'Rachel'
        assert note.created_at is not None
