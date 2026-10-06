# core/settings/base.py

from core.url_names import ACCOUNTS
from pathlib import Path
from decouple import config
from typing import cast


BASE_DIR = Path(__file__).resolve().parent.parent.parent
SECRET_KEY = config("SECRET_KEY") or "django-insecure-g-#*5w34-8=wbi_n0z$qaw60%33sc&aav^1+s^b0!0p-1z!b(k"
ALLOWED_HOSTS = []
PREVILEDGE_USERS = cast(str, config("PREVILEDGE_USERS", default="")).split(", ")

LOGIN_URL = ACCOUNTS.AUTH.LOGIN
LOGOUT_REDIRECT_URL = ACCOUNTS.AUTH.LOGIN
LOGIN_REDIRECT_URL = ACCOUNTS.DASHBOARD

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    
    "django.contrib.humanize",
    "django_extensions",
    "django_vite",
    "anymail",
    "mathfilters",
    
    "accounts.apps.AccountsConfig",
    "customers.apps.CustomersConfig",
    "products.apps.ProductsConfig",
    "invoices.apps.InvoicesConfig",
    "shared_tags.apps.SharedTagsConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    
    "middlewares.exception_request.ExceptionRequestMiddleware",
    "middlewares.enforce_onboarding.OnboardingEnforcementMiddleware",
    # "middlewares.guest_restriction.GuestRestrictionMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "core.context_processors.url_name_registry",
                "core.context_processors.template_context",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"


# Password validation
# https://docs.djangoproject.com/en/6.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/6.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Africa/Lagos"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.1/howto/static-files/

STATIC_URL = "/static/"
MEDIA_URL = "/media/"

STATICFILES_DIRS = [BASE_DIR / "static"]


# Email
# https://docs.djangoproject.com/en/6.1/topics/email/#topic-email-configuration

MAILERS = {
    "default": {
        "BACKEND": "django.core.mail.backends.smtp.EmailBackend",
        "OPTIONS": {
            "host": config("SMTP_HOST", default="salesiq.com.ng"),
            "port": config("SMTP_PORT", default=465, cast=int),
            "username": config("SMTP_USER", default=""),
            "password": config("SMTP_PASSWORD", default=""),
            "use_ssl": True,
        },
    },
    "anymail": {
        "BACKEND": "anymail.backends.resend.EmailBackend",
        "OPTIONS": {
            "api_key": config("RESEND_API_KEY"),
        },
    },
}
MAILER_EMS = "anymail"
ANYMAIL = {
    "REQUESTS_TIMEOUT": (5, 10),
}

DEFAULT_FROM_EMAIL = "SalesIQ <no-reply@notifications.salesiq.com.ng>"

AUTH_USER_MODEL = "accounts.CustomUserModel"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "error_context": {"()": "core.logging.ErrorContextFilter"},
    },
    "formatters": {
        "detailed": {
            "format": (
                "%(asctime)s %(levelname)s %(name)s | "
                "user=%(user_email)s business=%(business_code)s | "
                "at=%(error_loc)s | %(message)s"
            ),
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "plain": {
            "format": "%(asctime)s %(levelname)s %(name)s | %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "detailed",
            "filters": ["error_context"],
        },
        "console_plain": {
            "class": "logging.StreamHandler",
            "formatter": "plain",
        },
    },
    "root": {"handlers": ["console"], "level": "WARNING"},
    "loggers": {
        # Clear Django's default handlers so records go through root only (no duplicates)
        "django": {"handlers": [], "propagate": True},
        "django.server": {"handlers": ["console_plain"], "propagate": False},
    },
}

