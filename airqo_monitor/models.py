import json
import pytz

from django.db import models

from airqo_monitor.constants import PYTZ_KAMPALA_STRING


class ChannelType(models.Model):

    class Meta:
        db_table = 'channel_type'

    created_at = models.DateTimeField("date created", auto_now_add=True)
    name = models.TextField(null=False, db_index=True)
    friendly_name = models.TextField(null=False)
    data_format_json = models.TextField(null=False)  ## in json
    description = models.TextField(null=True)

    def __str__(self):
        return self.friendly_name

    @property
    def data_format(self):
        return json.loads(self.data_format_json)

    def save(self, *args, **kwargs):
        try:
            self.data_format
        except TypeError as e:
            raise ('This field must be in valid JSON: {}'.format(e))

        super(ChannelType, self).save(*args, **kwargs)


class Channel(models.Model):

    class Meta:
        db_table = 'channel'

    created_at = models.DateTimeField("date created", auto_now_add=True)
    channel_id = models.IntegerField(
        null=False,
        db_index=True,
        unique=True,
    )
    name = models.TextField(null=True)
    is_active = models.BooleanField(default=True)
    channel_type = models.ForeignKey(
        ChannelType,
        null=False,
        db_index=True,
        on_delete=models.DO_NOTHING,
    )

    def __str__(self):
        return '{}: {}'.format(self.channel_id, self.name)


class MalfunctionReason(models.Model):

    class Meta:
        db_table = 'malfunction_reason'

    name = models.TextField(
        null=False,
        db_index=True,
    )
    description = models.TextField(null=False)

    def __str__(self):
        return self.name

    @property
    def incidents(self):
        incident_ids = self.get_incident_ids()
        return Incident.objects.filter(
            id__in=list(incident_ids)
        ).all()


class Incident(models.Model):

    class Meta:
        db_table = 'incident'

    created_at = models.DateTimeField("date created", auto_now_add=True)
    resolved_at = models.DateTimeField(
        null=True,
        db_index=True,
    )
    channel = models.ForeignKey(
        Channel,
        null=False,
        db_index=True,
        on_delete=models.DO_NOTHING,
    )
    malfunction_reason = models.ForeignKey(
        MalfunctionReason,
        null=False,
        db_index=True,
        on_delete=models.DO_NOTHING,
    )

    def __str__(self):
        return '{}: {}'.format(
            self.channel.name,
            'resolved' if self.resolved_at else 'not resolved',
        )

    @property
    def local_created_at(self):
        local_tz = pytz.timezone(PYTZ_KAMPALA_STRING)
        return self.created_at.astimezone(local_tz)

    @property
    def local_resolved_at(self):
        local_tz = pytz.timezone(PYTZ_KAMPALA_STRING)
        utc_resolved_at = self.resolved_at
        return utc_resolved_at.astimezone(local_tz) if utc_resolved_at else None


class ChannelNote(models.Model):

    class Meta:
        db_table = 'channel_note'

    created_at = models.DateTimeField("date created", auto_now_add=True)
    channel = models.ForeignKey(
        Channel,
        null=False,
        db_index=True,
        on_delete=models.DO_NOTHING,
    )
    note = models.TextField(null=False)
    author = models.TextField(null=False)  ## who is leaving this note?

    def __str__(self):
        return '{} -{}'.format(self.note, self.author)

    @property
    def local_created_at(self):
        local_tz = pytz.timezone(PYTZ_KAMPALA_STRING)
        return self.created_at.astimezone(local_tz)
