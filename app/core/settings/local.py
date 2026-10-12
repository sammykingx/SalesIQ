# Django settings for local development environment
# core/settings/local.py

from .base import *
from decouple import config


DEBUG = config("DEBUG", default=False, cast=bool)
ALLOWED_DOMAINS = cast(str, config("ALLOWED_DOMAINS", default="")).split(", ")
ALLOWED_HOSTS = ALLOWED_DOMAINS or ["localhost"]
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_ROOT = BASE_DIR / "mediafiles"

DJANGO_VITE = {
    "default": {
        "dev_mode": DEBUG,
        "static_url_prefix": "" if DEBUG else "dist",
        "manifest_path": BASE_DIR / "static" / "dist" / "manifest.json",
    }
}
