from .base import *

DEBUG = False

ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=[])

SECRET_KEY = env("DJANGO_SECRET_KEY")
SITE_URL = ""

DATABASES["default"]["ATOMIC_REQUESTS"] = True  # noqa F405
DATABASES["default"]["CONN_MAX_AGE"] = env.int("CONN_MAX_AGE", default=15)  # noqa F405
DATABASES["default"]["ENGINE"] = "django.db.backends.postgresql"  # noqa F405

CORS_ALLOW_ALL_ORIGINS = True
DATA_UPLOAD_MAX_MEMORY_SIZE = 20 * 1024 * 1024  # 20Mb
