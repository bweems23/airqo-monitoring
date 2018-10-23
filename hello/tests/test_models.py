from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase, RequestFactory

from .views import index


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
        assert self.reason.incidents == [self.incident]
        assert self.incident.malfunction_reasons == [self.reason]