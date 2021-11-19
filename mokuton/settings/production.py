from .base import *

DEBUG = False

ALLOWED_HOSTS = [
    "localhost",
    "127.0.01",
    # Production domain/urls goes here
]

ALLOWED_HOSTS += env.list("DJANGO_ALLOWED_HOSTS", default=[])
SECRET_KEY = env("DJANGO_SECRET_KEY")
SITE_URL = ""


DATABASES["default"]["ATOMIC_REQUESTS"] = True  # noqa F405
DATABASES["default"]["CONN_MAX_AGE"] = env.int("CONN_MAX_AGE", default=15)  # noqa F405
DATABASES["default"]["ENGINE"] = "django.db.backends.postgresql"  # noqa F405

CORS_ALLOW_ALL_ORIGINS = True
