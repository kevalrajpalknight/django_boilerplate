import json
from datetime import timedelta
from pathlib import Path

from django.core.management.commands.runserver import Command as runserver

from decouple import Csv, config

BASE_DIR = Path(__file__).resolve().parent.parent.parent

BASE_URL = config("BASE_URL", default="127.0.0.1")

APPS_DIR = BASE_DIR / "config"


# ==============================================================================
# CORE SETTINGS
# ==============================================================================
ADDRESS = config("DJANGO_ADDRESS")
runserver.default_addr = ADDRESS

PORT = int(config("DJANGO_PORT"))
runserver.default_port = PORT

SECRET_KEY = config("DJANGO_SECRET_KEY", default="django-insecure$simple.settings.local")

DEBUG = config("DJANGO_DEBUG", default=True, cast=bool)

ALLOWED_HOSTS = config("DJANGO_ALLOWED_HOSTS", default="127.0.0.1,localhost", cast=Csv())

CSRF_TRUSTED_ORIGINS = config("DJANGO_CSRF_TRUSTED_ORIGINS", cast=Csv())

ADMINS = [("DEVELOPER", config("DJANGO_ADMINS"))]

MANAGERS = [("DEVELOPER", config("DJANGO_MANAGERS"))]

THIRD_PARTY_APPS = [
    {% if cookiecutter.use_drf == "y" %}
    "corsheaders",
    "rest_framework",
    "drf_yasg",
    {% endif %}
    {% if cookiecutter.use_simple_jwt == "y" %}
    "rest_framework_simplejwt",
    {% endif %}
    {% if cookiecutter.use_django_rq == "y" %}
    "django_rq",
    {% endif %}
]

LOCAL_APPS = [
    "core.apps.CoreConfig",
    "users.apps.UsersConfig",
]

INSTALLED_APPS = [
    {% if cookiecutter.use_jazzmin == "y" %}
    "jazzmin",
    {% endif %}
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
] + THIRD_PARTY_APPS + LOCAL_APPS

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

ROOT_URLCONF = "config.urls"

WSGI_APPLICATION = "config.wsgi.application"

AUTH_USER_MODEL = "users.User"

# ==============================================================================
# MIDDLEWARE SETTINGS
# ==============================================================================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    {% if cookiecutter.use_drf == "y" %}
    "corsheaders.middleware.CorsMiddleware",
    {% endif %}
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

{% if cookiecutter.use_simple_jwt == "y" %}
# ==============================================================================
# SESSION SETTINGS
# ==============================================================================
SESSION_COOKIE_AGE = 24 * 60 * 60  # 1 day in seconds
REMEMBER_ME_SESSION_COOKIE_AGE = 30 * 24 * 60 * 60  # 30 day in seconds
{% endif %}

# ==============================================================================
# TEMPLATES SETTINGS
# ==============================================================================

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR, "templates"],
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


# ==============================================================================
# DATABASES SETTINGS
# ==============================================================================

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("DATABASE_NAME"),
        "USER": config("DATABASE_USER"),
        "PASSWORD": config("DATABASE_PASSWORD"),
        "HOST": config("DATABASE_HOST"),
        "PORT": config("DATABASE_PORT"),
    }
}


# ==============================================================================
# AUTHENTICATION AND AUTHORIZATION SETTINGS
# ==============================================================================

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

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]

# ==============================================================================
# I18N AND L10N SETTINGS
# ==============================================================================

LANGUAGE_CODE = config("LANGUAGE_CODE", default="en-us")

TIME_ZONE = config("TIME_ZONE", default="UTC")

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATHS = [BASE_DIR / "locale"]


# ==============================================================================
# STATIC FILES SETTINGS
# ==============================================================================

STATIC_URL = "/static/"

STATIC_ROOT = BASE_DIR / "static"

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)


# ==============================================================================
# MEDIA FILES SETTINGS
# ==============================================================================

MEDIA_URL = "/media/"

MEDIA_ROOT = BASE_DIR / "media"


# ==============================================================================
# LOGGING SETTINGS
# ==============================================================================

DEFAULT_EXCEPTION_REPORTER_FILTER = "django.views.debug.SafeExceptionReporterFilter"
SERVER_KEY = "django.server"
LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        SERVER_KEY: {
            "()": "django.utils.log.ServerFormatter",
            "format": "[%(server_time)s] %(message)s",
        },
        "verbose": {"format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s"},
        "simple": {"format": "%(levelname)s %(message)s"},
    },
    "filters": {
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse",
        },
    },
    "handlers": {
        "server": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "django.server",
        },
        "console": {
            "level": "WARNING",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
            "filters": ["require_debug_true"],
        },
        "app_file": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "./app.log",
            "maxBytes": 1024 * 1024 * 5,  # 5 MB
            "backupCount": 5,
            "formatter": "verbose",
        },
        "error_file": {
            "level": "ERROR",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "./error.log",
            "maxBytes": 1024 * 1024 * 5,  # 5 MB
            "backupCount": 5,
            "formatter": "verbose",
            "filters": ["require_debug_false"],
        },
        "mail_admins": {
            "level": "ERROR",
            "class": "django.utils.log.AdminEmailHandler",
            "include_html": True,
            "formatter": "verbose",
            "filters": ["require_debug_false"],
        },
    },
    "loggers": {
        "django": {
            "handlers": ["app_file", "error_file"],
            "level": "INFO",
            "propagate": False,
        },
        SERVER_KEY: {
            "handlers": [
                "server",
                "app_file",
            ],
            "level": "INFO",
            "propagate": False,
        },
        "django.request": {
            "handlers": ["mail_admins", "error_file"],
            "level": "ERROR",
            "propagate": True,
        },
        "django.db.backends": {"handlers": ["app_file"], "level": "INFO"},
    },
}

# ==============================================================================
# THIRD PARTY SETTING
# ==============================================================================
{% if cookiecutter.use_drf == "y" %}
# Django Rest Framework
REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": config("DJANGO_PAGINATION_LIMIT", default=10, cast=int),
    "DEFAULT_RENDERER_CLASSES": (
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ),
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": (
        {% if cookiecutter.use_simple_jwt == "y" %}
            {% if cookiecutter.use_custom_simple_jwt == "y" %}
                "core.authentications.CustomJWTAuthentication",
            {% else %}
                "rest_framework_simplejwt.authentication.JWTAuthentication",
            {% endif %}
        {% endif %}
    ),
    "DEFAULT_SCHEMA_CLASS": "rest_framework.schemas.coreapi.AutoSchema",
}

# Cors Header Configuration
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = False

# Swagger
SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT Bearer token",
        },
    },
}

{% endif %}

{% if cookiecutter.use_jazzmin == "y" %}
# Jazzmin Configuration
JAZZMIN_SETTINGS = None
JAZZMIN_UI_TWEAKS = None

with open(BASE_DIR / "config" / "settings" / "jazzmin" / "configurations.json") as f:
    data = json.load(f)
    JAZZMIN_SETTINGS = {"show_ui_builder": DEBUG, **data}

with open(BASE_DIR / "config" / "settings" / "jazzmin" / "ui_tweaks.json") as f:
    data = json.load(f)
    JAZZMIN_UI_TWEAKS = {**data}

{% endif %}

{% if cookiecutter.use_simple_jwt == "y" %}
# Simple JWT
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=int(config("JWT_ACCESS_TOKEN_LIFETIME"))),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=int(config("JWT_REFRESH_TOKEN_LIFETIME"))),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": False,
    "ALGORITHM": config("JWT_ALGORITHM"),
    "VERIFYING_KEY": None,
    "AUDIENCE": None,
    "ISSUER": None,
    "JWK_URL": None,
    "LEEWAY": 0,
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "session_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",
    "JTI_CLAIM": "jti",
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=int(config("JWT_SLIDING_TOKEN_LIFETIME"))),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=int(config("JWT_SLIDING_TOKEN_REFRESH_LIFETIME"))),
    "SIGNING_KEY": config("DJANGO_SECRET_KEY"),
}
{% endif %}
