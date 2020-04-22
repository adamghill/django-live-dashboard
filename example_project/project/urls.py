from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles import views
from django.urls import include, path, re_path
from django_live_dashboard import urls


urlpatterns = [path("admin/", admin.site.urls), path("", include(urls))]

if settings.DEBUG:
    urlpatterns += (re_path(r"^static/(?P<path>.*)$", views.serve),)
