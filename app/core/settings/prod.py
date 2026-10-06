# Production settings for SalesIQ Django application
# These settings are optimized for a production environment, ensuring security, performance, and reliability.
# core/settings/prod.py

import os
from decouple import config
from typing import cast
from .base import *


DEBUG = False
ALLOWED_DOMAINS = cast(str, config("ALLOWED_DOMAINS", default="")).split(", ")
ALLOWED_HOSTS = ALLOWED_DOMAINS or []

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST", "localhost"),
        "PORT": "3306",
        "CONN_MAX_AGE": 120,
        "CONN_HEALTH_CHECKS": True,
        "OPTIONS": {
            "charset": "utf8mb4",
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES', innodb_lock_wait_timeout=5",
            "connect_timeout": 10,
            "read_timeout": 30,
            "write_timeout": 30,
            "isolation_level": "read committed",
        },
    }
}

DOCUMENT_ROOT = Path(
    cast(str, config("DOCUMENT_ROOT", default=(BASE_DIR)))
)
STATIC_ROOT = DOCUMENT_ROOT / "static"
MEDIA_ROOT = DOCUMENT_ROOT / "media"


DJANGO_VITE = {
    "default": {
        "dev_mode": False,
        "static_url_prefix": "dist",
        "manifest_path": BASE_DIR / "static" / "dist" / "manifest.json",
    }
}
