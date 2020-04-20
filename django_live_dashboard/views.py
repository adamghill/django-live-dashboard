from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render


@staff_member_required
def monitoring(request):
    websocket_host = settings.DJANGO_LIVE_DASHBOARD.get("WEBSOCKET_HOST", "localhost")
    refresh = settings.DJANGO_LIVE_DASHBOARD.get("CHART", {}).get("REFRESH", 1000)
    delay = settings.DJANGO_LIVE_DASHBOARD.get("CHART", {}).get("DELAY", 1000)
    duration = settings.DJANGO_LIVE_DASHBOARD.get("CHART", {}).get("DURATION", 100000)
    pubsub_channel = settings.DJANGO_LIVE_DASHBOARD.get("REDIS", {}).get(
        "PUBSUB_CHANNEL", "django_live_dashboard:stats"
    )

    return render(
        request,
        "django_live_dashboard/monitoring.html",
        {
            "pubsub_channel": pubsub_channel,
            "websocket_host": websocket_host,
            "refresh": refresh,
            "delay": delay,
            "duration": duration,
        },
    )
