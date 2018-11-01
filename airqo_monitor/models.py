from django.db import models


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
