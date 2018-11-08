from django.test import TestCase

from airqo_monitor.management.commands.utils import create_basic_test_data
from airqo_monitor.models import (
    ChannelType,
    GlobalVariable,
    MalfunctionReason,
)


class TestIncidentModel(TestCase):
    def setUp(self):
        pass

    def test_create_basic_test_data(self):
        create_basic_test_data()

        assert ChannelType.objects.count() == 1
        assert GlobalVariable.objects.count() == 8
        assert MalfunctionReason.objects.count() == 4
