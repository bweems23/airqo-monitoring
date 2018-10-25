from rest_framework import serializers

from airqo_monitor.models import Channel, Incident, MalfunctionReason


class ChannelSerializer(serializers.ModelSerializer):
    channel_id = serializers.IntegerField()
    name = serializers.CharField(max_length=100)

    class Meta:
        model = Channel
        fields = (
            'channel_id',
            'name',
        )


class MalfunctionReasonSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=500)

    class Meta:
        model = MalfunctionReason
        fields = (
            'name',
            'description',
        )


class IncidentSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField()
    resolved_at = serializers.DateTimeField()
    malfunction_reasons = MalfunctionReasonSerializer(many=True)

    class Meta:
        model = Incident
        fields = (
            'created_at',
            'resolved_at',
            'malfunction_reasons',
        )
