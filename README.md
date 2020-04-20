# django_live_dashboard

Inspired by Phoenix's LiveViewDashboard; uses redis publisher-subscriber, chart.js, and alpine.js.

# Requires
1. Python 3.6+
1. Django 3.0+
1. Django to be run via `ASGI` for websockets

# Install
1. `pip install django-live-dashboard` or `poetry add django-live-dashboard`
1. Update current `asgi.py` or use the `asgi.py` in the repo as an example
1. Add `"django_live_dashboard",` to `INSTALLED_APPS` in settings file
1. Add `"django_live_dashboard.middleware.DjangoLiveDashboardMiddleware",` to beginning of the `MIDDLEWARE` list in settings file
1. Add `DJANGO_LIVE_DASHBOARD` configuration to settings file (see details below)
1. Add to default `urls.py`: `path("admin/", include(django_live_dashboard_urls))`
1. Run your server with something like `uvicorn project.asgi:application --port=8000`

# Settings
Configuration is in a `DJANGO_LIVE_DASHBOARD` setting.

## Example
```python
DJANGO_LIVE_DASHBOARD = {
    "ENABLED": True,
    "WEBSOCKET_HOST": 'localhost:8000',
    "TOTAL_TIME_CUTOFF": 0.5,
    "REDIS": {
        "HOST": "localhost",
        "PORT": 6379,
        "DB": 0,
        "PUBSUB_CHANNEL": "django_live_dashboard:stats"
    },
    "CHART": {
        "REFRESH": 1000,
        "DELAY": 1000,
        "DURATION": 100000,
    }
}
```

## ENABLED
Whether any statistics should be logged. Defaults to `DEBUG`.

## WEBSOCKET_HOST
The host that the websocket should listen to. Defaults to `localhost`.

## TOTAL_TIME_CUTOFF
How long a request should take in seconds before getting logged. For example, if the value is 0.75, any request that takes longer than three quarters of a second will get graphed. Defaults to `0.5`.

## REDIS
Redis configuration with standard `HOST`, `PORT`, and `DB` settings in a dictionary.

### HOST 
The host of the redis server. Defaults to `localhost`.

### PORT
THe port of the redis server. Defaults to `6379`.

### DB
The database of the redis server. Defaults to `0`.

## CHART
Configuration for the streaming `chart.js` plugin.

### DELAY
Delay in milliseconds of the `chart.js` which helps to make the drawing more fluid and smooth. Defaults to 1000.

### DURATION
Time duration in milliseconds of how much data should be charted. Defaults to 100000.

### REFRESH
How often the chart should try to refresh its data. Defaults to 1000.

# Local dev
1. `poetry build`
1. `pip install -U django-live-dashboard/dist/django_live_dashboard-0.1.0-py3-none-any.whl`
