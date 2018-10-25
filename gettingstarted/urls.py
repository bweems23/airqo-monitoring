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
    path("db/", airqo_monitor.views.db, name="db"),
    path("admin/", admin.site.urls),
    path("channels/<int:channel_id>/", airqo_monitor.views.channel_detail, name="channel_detail")
]
