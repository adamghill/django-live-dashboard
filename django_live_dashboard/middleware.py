from time import time

from django.conf import settings
from django.db import connection

import orjson
import redis


class DjangoLiveDashboardMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.is_enabled = settings.DJANGO_LIVE_DASHBOARD.get("ENABLED", settings.DEBUG)

        if self.is_enabled:
            redis_host = settings.DJANGO_LIVE_DASHBOARD.get("REDIS", {}).get(
                "HOST", "localhost"
            )
            redis_port = settings.DJANGO_LIVE_DASHBOARD.get("REDIS", {}).get(
                "PORT", 6379
            )
            redis_db = settings.DJANGO_LIVE_DASHBOARD.get("REDIS", {}).get("DB", 0)

            self.redis_connection = redis.Redis(
                host=redis_host, port=redis_port, db=redis_db,
            )

    def __call__(self, request):
        if self.is_enabled:
            # Get initial data
            start = time()
            initial_database_query_count = len(connection.queries)

            response = self.get_response(request)

            # Get data after the response has been created
            total_time = time() - start
            total_time_cutoff = settings.DJANGO_LIVE_DASHBOARD.get(
                "TOTAL_TIME_CUTOFF", 0.5
            )

            if total_time > total_time_cutoff:
                db_queries = len(connection.queries) - initial_database_query_count
                db_time = 0.0

                if db_queries:
                    db_time = sum(
                        [
                            float(q["time"])
                            for q in connection.queries[initial_database_query_count:]
                        ],
                    )

                python_time = total_time - db_time
                url = request.path

                stats = {
                    "url": url,
                    "totalTime": total_time,
                    "pythonTime": python_time,
                    "dbTime": db_time,
                    "dbQueries": (db_queries - initial_database_query_count),
                }

                pubsub_channel = settings.DJANGO_LIVE_DASHBOARD.get("REDIS", {}).get(
                    "PUBSUB_CHANNEL", "django_live_dashboard:stats"
                )
                self.redis_connection.publish(pubsub_channel, orjson.dumps(stats))

        return response
