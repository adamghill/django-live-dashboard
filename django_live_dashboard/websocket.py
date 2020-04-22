import asyncio

import aioredis
import orjson
from box import Box

from .conf import Settings


async def reader(channel, send):
    while await channel.wait_message():
        message = await channel.get_json()
        await send(
            {"type": "websocket.send", "text": orjson.dumps(message).decode("utf-8")}
        )


async def websocket_application(scope, receive, send):
    settings = Box(Settings().DJANGO_LIVE_DASHBOARD)
    redis_host = settings.REDIS.HOST
    redis_port = settings.REDIS.PORT
    pubsub_channel = settings.REDIS.PUBSUB_CHANNEL

    subscriber = await aioredis.create_redis(f"redis://{redis_host}:{redis_port}")
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
