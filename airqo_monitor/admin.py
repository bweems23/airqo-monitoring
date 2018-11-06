from django.contrib import admin

from airqo_monitor.models import (
	Channel,
	ChannelNote,
	ChannelType,
	GlobalVariable,
	Incident,
	MalfunctionReason,
)

# Register your models here.
admin.site.register(Channel)
admin.site.register(ChannelNote)
admin.site.register(ChannelType)
admin.site.register(GlobalVariable)
admin.site.register(Incident)
admin.site.register(MalfunctionReason)
