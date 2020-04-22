from django.conf import settings

import appsettings


REDIS_DEFAULTS = {
    "HOST": "localhost",
    "PORT": 6379,
    "DB": 0,
    "PUBSUB_CHANNEL": "django_live_dashboard:stats",
}
CHART_DEFAULTS = {"REFRESH": 1000, "DELAY": 1000, "DURATION": 10000}


class Settings(appsettings.AppSettings):
    DJANGO_LIVE_DASHBOARD = appsettings.NestedDictSetting(
        settings=dict(
            ENABLED=appsettings.BooleanSetting(default=False),
            WEBSOCKET_HOST=appsettings.StringSetting(default="localhost:8000"),
            TOTAL_TIME_CUTOFF=appsettings.FloatSetting(default=0.5),
            REDIS=appsettings.NestedDictSetting(
                settings=dict(
                    HOST=appsettings.StringSetting(default=REDIS_DEFAULTS["HOST"]),
                    PORT=appsettings.IntegerSetting(default=REDIS_DEFAULTS["PORT"]),
                    DB=appsettings.IntegerSetting(default=REDIS_DEFAULTS["DB"]),
                    PUBSUB_CHANNEL=appsettings.StringSetting(
                        default=REDIS_DEFAULTS["PUBSUB_CHANNEL"]
                    ),
                ),
                default=REDIS_DEFAULTS,
            ),
            CHART=appsettings.NestedDictSetting(
                settings=dict(
                    REFRESH=appsettings.IntegerSetting(
                        default=CHART_DEFAULTS["REFRESH"]
                    ),
                    DELAY=appsettings.IntegerSetting(default=CHART_DEFAULTS["DELAY"]),
                    DURATION=appsettings.IntegerSetting(
                        default=CHART_DEFAULTS["DURATION"]
                    ),
                ),
                default=CHART_DEFAULTS,
            ),
        ),
        default={
            "ENABLED": False,
            "WEBSOCKET_HOST": "localhost:8000",
            "TOTAL_TIME_CUTOFF": 0.5,
            "REDIS": REDIS_DEFAULTS,
            "CHART": CHART_DEFAULTS,
        },
    )
