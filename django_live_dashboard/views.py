from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render

from box import Box

from .conf import Settings


@staff_member_required
def monitoring(request):
    settings = Box(Settings().DJANGO_LIVE_DASHBOARD)

    return render(
        request,
        "django_live_dashboard/monitoring.html",
        {
            "pubsub_channel": settings.REDIS.PUBSUB_CHANNEL,
            "websocket_host": settings.WEBSOCKET_HOST,
            "refresh": settings.CHART.REFRESH,
            "delay": settings.CHART.DELAY,
            "duration": settings.CHART.DURATION,
        },
    )
