from django.contrib import admin

from airqo_monitor.models import (
	Channel,
	ChannelNote,
	Incident,
	MalfunctionReason,
)

# Register your models here.
admin.site.register(Channel)
admin.site.register(ChannelNote)
admin.site.register(Incident)
admin.site.register(MalfunctionReason)
