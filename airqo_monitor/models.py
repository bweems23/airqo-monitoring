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


class Incident(models.Model):

    class Meta:
        db_table = 'incident'

    created_at = models.DateTimeField("date created", auto_now_add=True)
    resolved_at = models.DateTimeField(null=True)
    channel = models.ForeignKey(
        Channel,
        null=False,
        db_index=True,
        on_delete=models.DO_NOTHING,
    )

    def __str__(self):
        return '{}: {}'.format(
            self.channel.name,
            'resolved' if self.resolved_at else 'not resolved',
        )

    def get_malfunction_reason_ids(self):
        return IncidentMalfunctionReasonLink.objects.filter(
            incident=self
        ).values_list('malfunction_reason_id', flat=True)

    @property
    def malfunction_reasons(self):
        reason_ids = self.get_malfunction_reason_ids()
        return MalfunctionReason.objects.filter(
            id__in=list(reason_ids)
        ).all()


class MalfunctionReason(models.Model):

    class Meta:
        db_table = 'malfunction_reason'

    name = models.TextField(null=False)
    description = models.TextField(null=False)

    def __str__(self):
        return self.name

    def get_incident_ids(self):
        return IncidentMalfunctionReasonLink.objects.filter(
            malfunction_reason=self
        ).values_list('incident_id', flat=True)

    @property
    def incidents(self):
        incident_ids = self.get_incident_ids()
        return Incident.objects.filter(
            id__in=list(incident_ids)
        ).all()


class IncidentMalfunctionReasonLink(models.Model):

    class Meta:
        db_table = 'incident_malfunction_reason_link'
        unique_together = ('incident', 'malfunction_reason')

    incident = models.ForeignKey(
        Incident,
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
        return 'Incident ID {}: {}'.format(self.incident_id, self.malfunction_reason)


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
