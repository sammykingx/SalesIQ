from .base import *
from decouple import config


DEBUG = config("DEBUG", default=False, cast=bool)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}


PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]


MAILERS = {
    "default": {"BACKEND": "django.core.mail.backends.locmem.EmailBackend", "OPTIONS": {}},
    "anymail": {"BACKEND": "django.core.mail.backends.locmem.EmailBackend", "OPTIONS": {}},
}

MAILER_EMS = "default"


DJANGO_VITE = {
    "default": {
        "dev_mode": False,
        "manifest_path": BASE_DIR / "static" / "dist" / "manifest.json",
    }
}
