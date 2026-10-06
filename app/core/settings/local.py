# Django settings for local development environment
# core/settings/local.py

from .base import *


DEBUG = True
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
        "dev_mode": True,
        "manifest_path": BASE_DIR / "static" / "dist" / "manifest.json",
    }
}
