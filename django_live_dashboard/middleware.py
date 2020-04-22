from time import time

from django.db import connection

import orjson
import redis
from box import Box

from .conf import Settings


class DjangoLiveDashboardMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.settings = Box(Settings().DJANGO_LIVE_DASHBOARD)

        if self.settings.ENABLED:
            redis_host = self.settings.REDIS.HOST
            redis_port = self.settings.REDIS.PORT
            redis_db = self.settings.REDIS.DB

            self.redis_connection = redis.Redis(
                host=redis_host, port=redis_port, db=redis_db,
            )

    def __call__(self, request):
        if not self.settings.ENABLED:
            return self.get_response(request)

        # Get initial data
        start = time()
        initial_database_query_count = len(connection.queries)

        response = self.get_response(request)

        # Get data after the response has been created
        total_time = time() - start
        total_time_cutoff = self.settings.TOTAL_TIME_CUTOFF or 0

        if total_time > total_time_cutoff:
            database_queries = len(connection.queries) - initial_database_query_count
            database_time = 0.0

            if database_queries:
                database_time = sum(
                    [
                        float(q["time"])
                        for q in connection.queries[initial_database_query_count:]
                    ],
                )

            python_time = total_time - database_time
            url = request.path

            stats = {
                "url": url,
                "totalTime": total_time,
                "pythonTime": python_time,
                "databaseTime": database_time,
                "databaseQueries": (database_queries - initial_database_query_count),
            }

            pubsub_channel = self.settings.REDIS.PUBSUB_CHANNEL
            self.redis_connection.publish(pubsub_channel, orjson.dumps(stats))

        return response
