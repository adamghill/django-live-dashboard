from django.urls import path

from .views import monitoring


app_name = "django_live_dashboard"

urlpatterns = (path("monitoring/", monitoring, name="monitoring"),)
