import asyncio
import orjson

import aioredis
from django.conf import settings


async def reader(channel, send):
    while await channel.wait_message():
        message = await channel.get_json()
        await send(
            {"type": "websocket.send", "text": orjson.dumps(message).decode("utf-8")}
        )


async def websocket_application(scope, receive, send):
    redis_host = settings.DJANGO_LIVE_DASHBOARD.get("REDIS", {}).get(
        "HOST", "localhost"
    )
    redis_port = settings.DJANGO_LIVE_DASHBOARD.get("REDIS", {}).get("PORT", 6379)

    subscriber = await aioredis.create_redis(f"redis://{redis_host}:{redis_port}")
    pubsub_channel = settings.DJANGO_LIVE_DASHBOARD.get("REDIS", {}).get(
        "PUBSUB_CHANNEL", "django_live_dashboard:stats"
    )
    response = await subscriber.subscribe(pubsub_channel)

    while True:
        event = await receive()
        channel = response[0]
        task = None

        if event["type"] == "websocket.connect":
            await send({"type": "websocket.accept"})

        if event["type"] == "websocket.disconnect":
            await subscriber.unsubscribe(pubsub_channel)

            if task:
                await task

            subscriber.close()
            break

        if event["type"] == "websocket.receive":
            if event["text"] == pubsub_channel:
                task = asyncio.ensure_future(reader(channel, send))
