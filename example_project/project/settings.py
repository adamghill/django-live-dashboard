import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = "px1xyx=o(p*9&a$(w1+59calf9%83@eaxsb^%%me02^$iriz=@"
DEBUG = True
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "0.0.0.0"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_live_dashboard",
]

MIDDLEWARE = [
    "django_live_dashboard.middleware.DjangoLiveDashboardMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "example_project.project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}

STATIC_URL = "/static/"

DJANGO_LIVE_DASHBOARD = {
    "ENABLED": True,
    "WEBSOCKET_HOST": "localhost:8000",
    "TOTAL_TIME_CUTOFF": 0,
    "REDIS": {
        "HOST": "localhost",
        "PORT": 6379,
        "DB": 0,
        "PUBSUB_CHANNEL": "django_live_dashboard:stats",
    },
    "CHART": {"REFRESH": 1000, "DELAY": 1000, "DURATION": 100000},
}
