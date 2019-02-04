from django.urls import path, include

from django.contrib import admin

admin.autodiscover()

import airqo_monitor.views

# To add a new path, first import the app:
# import blog
#
# Then add the new path:
# path('blog/', blog.urls, name="blog")
#
# Learn more here: https://docs.djangoproject.com/en/2.1/topics/http/urls/

urlpatterns = [
    path("", airqo_monitor.views.index, name="index"),
    path("incidents/", airqo_monitor.views.incidents, name="incidents"),
    path("db/", airqo_monitor.views.db, name="db"),
    path("admin/", admin.site.urls),
    path("channels/<int:channel_id>/", airqo_monitor.views.channel_detail, name="channel_detail"),
    path("channel_notes/", airqo_monitor.views.channel_notes, name="channel_note"),
    path("update_incidents/", airqo_monitor.views.update_incidents, name='update_incidents'),
    path("channel_types/", airqo_monitor.views.channel_types_list, name='all_channels_list'),
    path("channel_types/<str:channel_type>/", airqo_monitor.views.channel_type_channels_list, name='channels_list'),
    path("heatmap/", airqo_monitor.views.heatmap, name="heatmap"),
    path("heatmap/<str:channel_ids>/", airqo_monitor.views.heatmap_with_filter, name="heatmap_with_filter"),
]
