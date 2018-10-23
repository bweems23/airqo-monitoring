from django.db import models


class Greeting(models.Model):
    when = models.DateTimeField("date created", auto_now_add=True)


class Incident(models.Model):

    class Meta:
        db_table = 'incident'

    created_at = models.DateTimeField("date created", auto_now_add=True)
    channel_id = models.IntegerField(null=False, db_index=True)

    def malfunction_reasons(self):
        return IncidentMalfunctionReasonLink.objects.filter(incident=self).all()


class MalfunctionReason(models.Model):

    class Meta:
        db_table = 'malfunction_reason'

    name = models.TextField(null=False)
    description = models.TextField(null=False)

    def incidents(self):
        return IncidentMalfunctionReasonLink.objects.filter(malfunction_reason=self)


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