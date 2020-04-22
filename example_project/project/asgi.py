# -*- mode: python -*-
# vi: set ft=python :
import os

from django.core.asgi import get_asgi_application
from django_live_dashboard.websocket import websocket_application


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "example_project.project.settings")

django_application = get_asgi_application()

print("asgi got loaded")


async def application(scope, receive, send):
    if scope["type"] == "http":
        await django_application(scope, receive, send)
    elif scope["type"] == "websocket":
        print("got websocket")
        await websocket_application(scope, receive, send)
    else:
        raise NotImplementedError(f"Unknown scope type {scope['type']}")
