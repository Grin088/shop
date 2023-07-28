"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 4.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
from datetime import timedelta
from pathlib import Path
from urllib.parse import urlparse
from dotenv import dotenv_values
from django.utils.translation import gettext_lazy as _

import dj_database_url

config = dotenv_values(os.path.join("..", ".env"))

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
AUTH_USER_MODEL = "users.CustomUser"

CART_SESSION_ID = "cart"

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-=e-i4dlx_qq&ra7un4)u8bdr#08q)gc_*yyy4@7--kt(0(p#!("

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    # django apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_extensions",
    "django_jinja",
    "rest_framework",
    "taggit",
    # custom apps
    "products",
    "shops",
    "users",
    "catalog",
    "cart",
    "django_celery_beat",
    "django_celery_results",
    "discounts",
    "site_settings",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django_jinja.backend.Jinja2",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": ["cart.context_processors.cart"],
            "match_extension": ".jinja2",
            "match_regex": None,
            "app_dirname": "templates",
            # Can be set to "jinja2.Undefined" or any other subclass.
            "undefined": None,
            "newstyle_gettext": True,
            "tests": {
                # "mytest": "path.to.my.test",
            },
            "filters": {
                # "myfilter": "path.to.my.filter",
            },
            "globals": {
                # "myglobal": "path.to.my.globalfunc",
            },
            "constants": {
                # "foo": "bar",
            },
            "policies": {
                # "ext.i18n.trimmed": True,
            },
            "extensions": [
                "jinja2.ext.do",
                "jinja2.ext.loopcontrols",
                "jinja2.ext.i18n",
                "django_jinja.builtins.extensions.CsrfExtension",
                "django_jinja.builtins.extensions.CacheExtension",
                "django_jinja.builtins.extensions.DebugExtension",
                "django_jinja.builtins.extensions.TimezoneExtension",
                "django_jinja.builtins.extensions.UrlsExtension",
                "django_jinja.builtins.extensions.StaticFilesExtension",
                "django_jinja.builtins.extensions.DjangoFiltersExtension",
            ],
            "bytecode_cache": {
                "name": "default",
                "backend": "django_jinja.cache.BytecodeCache",
                "enabled": False,
            },
            "autoescape": True,
            "auto_reload": DEBUG,
            "translation_engine": "django.utils.translation",
        },
    },
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {"default": dj_database_url.parse(config["DATABASE_URL"])}

REDIS_URL = config["REDIS_URL"]
CACHE_CONSTANT = 600
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
        "KEY_PREFIX": "example",
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"
LANGUAGES = (("en", _("Английский")), ("ru", _("Русский")))

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, "/static")

STATIC_URL = "/static/"

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]


MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "uploads"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# settings for send email
EMAIL_USE_TLS = True
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_HOST_USER = "email"
EMAIL_HOST_PASSWORD = "password"

# Always use IPython for shell_plus
SHELL_PLUS = "ipython"
SHELL_PLUS_PRINT_SQL = True

# CELERY
CELERY_BROKER_URL = REDIS_URL
CELERY_TASK_TRACK_STARTED = True
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"
CELERY_BROKER_TRANSPORT_OPTION = {"visibility_timeout": 3600}
CELERY_RESULT_BACKEND = "django-db"
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TASK_DEFAULT_QUEUE = "default"
CELERY_BEAT_SCHEDULE = {
    "process_payment_queue": {
        "task": "market.shops.tasks.process_payment_queue",
        "schedule": timedelta(seconds=60),
    }
}

IMPORT_DONE = BASE_DIR / "imports" / "successful_imports"
IMPORT_FAIL = BASE_DIR / "imports" / "failed_imports"
IMPORT_LOGS = BASE_DIR / "imports" / "logs"

os.makedirs(IMPORT_DONE, exist_ok=True)
os.makedirs(IMPORT_FAIL, exist_ok=True)
os.makedirs(IMPORT_LOGS, exist_ok=True)

# transferring session storage to Redis
SESSION_ENGINE = "redis_sessions.session"
url = urlparse(REDIS_URL)
SESSION_REDIS = {
    "host": url.hostname,
    "port": url.port,
    "db": 0,
    "password": None,
    "prefix": "redis://",
    "socket_timeout": 1,
    "retry_on_timeout": False,
}

# maximum comparison list length
MAX_COMP_LIST_LEN = 3
