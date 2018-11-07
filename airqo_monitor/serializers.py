from datetime import datetime
from rest_framework import serializers

from airqo_monitor.models import (
    Channel,
    ChannelNote,
    ChannelType,
    Incident,
    MalfunctionReason,
)


class ChannelTypeSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100)
    friendly_name = serializers.CharField(max_length=100)

    class Meta:
        model = ChannelType
        fields = (
            'name',
            'friendly_name',
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
    malfunction_reason = MalfunctionReasonSerializer()

    class Meta:
        model = Incident
        fields = (
            'created_at',
            'resolved_at',
            'malfunction_reason',
        )


class ChannelSerializer(serializers.ModelSerializer):
    channel_id = serializers.IntegerField()
    name = serializers.CharField(max_length=100)
    active_incidents = serializers.SerializerMethodField()

    def get_active_incidents(self, obj):
        incidents = Incident.objects.filter(channel=obj, resolved_at__isnull=True)
        return IncidentSerializer(incidents, many=True).data

    class Meta:
        model = Channel
        fields = (
            'channel_id',
            'name',
            'active_incidents',
        )


class ChannelNoteSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField()
    note = serializers.CharField(max_length=500)
    author = serializers.CharField(max_length=100)

    class Meta:
        model = ChannelNote
        fields = (
            'created_at',
            'note',
            'author',
        )


class ChannelHistorySerializer(serializers.Serializer):
    object_type = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    note = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    resolved_at = serializers.SerializerMethodField()
    malfunction_reason = serializers.SerializerMethodField()

    def get_object_type(self, obj):
        if isinstance(obj, ChannelNote):
            return 'channel_note'
        if isinstance(obj, Incident):
            return 'incident'

    def get_note(self, obj):
        object_type = self.get_object_type(obj)
        if object_type == 'channel_note':
            return obj.note
        if object_type == 'incident':
            return None

    def get_author(self, obj):
        object_type = self.get_object_type(obj)
        if object_type == 'channel_note':
            return obj.author
        if object_type == 'incident':
            return None

    def get_created_at(self, obj):
        return datetime.strftime(obj.local_created_at,'%d/%m/%Y at %H:%M')

    def get_resolved_at(self, obj):
        object_type = self.get_object_type(obj)
        if object_type == 'channel_note':
            return None
        if object_type == 'incident':
            resolved_at = obj.local_resolved_at
            if resolved_at:
                return datetime.strftime(resolved_at,'%d/%m/%Y at %H:%M')
            else:
                return None

    def get_malfunction_reason(self, obj):
        object_type = self.get_object_type(obj)
        if object_type == 'channel_note':
            return None
        if object_type == 'incident':
            reason = obj.malfunction_reason
            return MalfunctionReasonSerializer(reason).data

    class Meta:
        fields = (
            'object_type',
            'created_at',
            'note',
            'author',
            'resolved_at',
            'malfunction_reason',
        )
