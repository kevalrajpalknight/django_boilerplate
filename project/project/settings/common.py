import os
from datetime import timedelta
from distutils.util import strtobool
import dj_database_url
from configurations import Configuration
from django.core.management.commands.runserver import Command as runserver

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_URL = os.environ.get('BASE_URL', )


class Common(Configuration):
    runserver.default_addr = os.environ.get('DJANGO_ADDRESS', '127.0.0.1')
    runserver.default_port = int(os.environ.get('DJANGO_PORT', 8000))

    INSTALLED_APPS = (
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',

        # Third party apps
        "corsheaders",  # for Cross-Origin Resource Sharing
        'rest_framework',  # utilities for rest apis
        'rest_framework.authtoken',  # token authentication
        'django_filters',  # for filtering rest endpoints
        'rest_framework_simplejwt',  # for the JWT authentication
        'drf_yasg', # for Swagger Open API

        'core.apps.CoreConfig',
        'user.apps.UserConfig',
    )

    # https://docs.djangoproject.com/en/2.0/topics/http/middleware/
    MIDDLEWARE = (
        "django.middleware.security.SecurityMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        'corsheaders.middleware.CorsMiddleware',
        'django.middleware.common.CommonMiddleware',
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",

        # To send broken link notification to MANAGERS
        # https://docs.djangoproject.com/en/4.1/ref/middleware/#django.middleware.common.BrokenLinkEmailsMiddleware
        "django.middleware.common.BrokenLinkEmailsMiddleware",

        # To validate the token signature and authenticate each request.
        "core.middleware.JWTMiddleware",

    )

    ROOT_URLCONF = 'project.urls'
    SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
    WSGI_APPLICATION = 'project.wsgi.application'

    # Email
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

    ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS').split(",")

    # A list of all the people who get code error notifications.
    # Django emails these people the details of exceptions raised in the request/response cycle.
    # https://docs.djangoproject.com/en/4.1/ref/settings/#std-setting-ADMINS

    ADMINS = [
        ('Organization', os.environ.get('ORGANIZATION')),
        ('DevOps', os.environ.get('DEVOPS')),
        ('TeamLeader', os.environ.get('QA')),
        ('Developer', os.environ.get('DEVELOPER')),
    ]

    # A list in the same format as ADMINS that specifies who should get broken link notifications.
    # https://docs.djangoproject.com/en/4.1/ref/settings/#std-setting-MANAGERS

    MANAGERS = [
        ('Developer', os.environ.get('DEVELOPER')),
    ]

    # Server Email
    # The email address that error messages come from, such as those sent to ADMINS and MANAGERS.
    # https://docs.djangoproject.com/en/4.1/ref/settings/#server-email

    SERVER_EMAIL = os.environ.get("SERVER_EMAIL")

    # Postgres
    DATABASES = {
        'default': dj_database_url.config(
            default=os.environ.get('DATABASE_URI'),
            conn_max_age=int(os.environ.get('POSTGRES_CONN_MAX_AGE', 600))
        )
    }

    # General
    APPEND_SLASH = False
    TIME_ZONE = 'UTC'
    DATETIME_FORMAT = "%Y-%m-%d%H:%M:%S"
    LANGUAGE_CODE = 'en-us'

    # If you set this to False, Django will make some optimizations so as not
    # to load the internationalization machinery.
    USE_I18N = False
    USE_L10N = False
    USE_TZ = False

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/2.0/howto/static-files/
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')
    STATICFILES_DIRS = []
    STATIC_URL = '/static/'
    STATICFILES_FINDERS = (
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    )

    # Media files
    MEDIA_ROOT = os.path.join(BASE_DIR , 'media')
    MEDIA_URL = '/media/'

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': STATICFILES_DIRS,
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        },
    ]

    # Set DEBUG to False as a default for safety
    # https://docs.djangoproject.com/en/dev/ref/settings/#debug
    DEBUG = strtobool(os.environ.get('DJANGO_DEBUG', 'no'))

    # Password Validation
    # https://docs.djangoproject.com/en/2.0/topics/auth/passwords/#module-django.contrib.auth.password_validation
    AUTH_PASSWORD_VALIDATORS = [
        {
            'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
        },
    ]

    AUTH_USER_MODEL = 'user.User'

    AUTHENTICATION_BACKENDS = [
        # Custom Authentication Backend
        'django.contrib.auth.backends.ModelBackend',
    ]

    # Logging
    
    DEFAULT_EXCEPTION_REPORTER_FILTER = 'django.views.debug.SafeExceptionReporterFilter'
    SERVER_KEY = "django.server"
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            SERVER_KEY: {
                '()': 'django.utils.log.ServerFormatter',
                'format': '[%(server_time)s] %(message)s',
            },
            'verbose': {
                'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
            },
            'simple': {
                'format': '%(levelname)s %(message)s'
            },
        },
        'filters': {
            'require_debug_true': {
                '()': 'django.utils.log.RequireDebugTrue',
            },
        },
        'handlers': {
            SERVER_KEY: {
                'level': 'INFO',
                'class': 'logging.StreamHandler',
                'formatter': SERVER_KEY,
            },
            'console': {
                'level': 'INFO',
                'class': 'logging.StreamHandler',
                'formatter': 'verbose'
            },
            'file': {
                'level': 'INFO',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': '../app.log',
                'maxBytes': 1024 * 1024 * 5,  # 5 MB
                'backupCount': 5,
                'formatter': 'verbose'
            },
            'mail_admins': {
                'level': 'ERROR',
                'class': 'django.utils.log.AdminEmailHandler',
                'include_html': True,  # Include HTML content in email body
                'formatter': 'verbose'  # Use verbose formatter for email output
            }
        },
        'loggers': {
            'django': {
                'handlers': ['console', 'file'],
                'level': 'INFO',
                'propagate': True,
            },
            SERVER_KEY: {
                'handlers': [SERVER_KEY, 'file',],
                'level': 'INFO',
                'propagate': False,
            },
            'django.request': {
                'handlers': ['mail_admins', 'file'],
                'level': 'ERROR',
                'propagate': False,
            },
            'django.db.backends': {
                'handlers': ['file'],
                'level': 'INFO'
            },
            'myapp': {  # Add a custom logger for your app
                'handlers': ['console', 'file'],
                'level': 'INFO',
                'propagate': True,
            },
        }
    }

    # Django Rest Framework
    REST_FRAMEWORK = {
        'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
        'PAGE_SIZE': int(os.environ.get('DJANGO_PAGINATION_LIMIT', 10)),
        'DEFAULT_RENDERER_CLASSES': (
            'rest_framework.renderers.JSONRenderer',
            'rest_framework.renderers.BrowsableAPIRenderer',
        ),
        'DEFAULT_PERMISSION_CLASSES': [
            'rest_framework.permissions.IsAuthenticated',
        ],
        'DEFAULT_AUTHENTICATION_CLASSES': (
            'core.authentications.CustomJWTAuthentication',
        )
    }

    # Django Rest Framework Simple JWT
    # https://django-rest-framework-simplejwt.readthedocs.io/en/latest/settings.html#

    SIMPLE_JWT = {
        'ACCESS_TOKEN_LIFETIME': timedelta(minutes=int(os.environ.get('JWT_ACCESS_TOKEN_LIFETIME'))),
        'REFRESH_TOKEN_LIFETIME': timedelta(days=int(os.environ.get('JWT_REFRESH_TOKEN_LIFETIME'))),
        'ROTATE_REFRESH_TOKENS': False,
        'BLACKLIST_AFTER_ROTATION': False,
        'UPDATE_LAST_LOGIN': False,

        'ALGORITHM': os.environ.get('JWT_ALGORITHM'),
        'VERIFYING_KEY': None,
        'AUDIENCE': None,
        'ISSUER': None,
        'JWK_URL': None,
        'LEEWAY': 0,

        'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
        'USER_ID_FIELD': 'id',
        'USER_ID_CLAIM': 'session_id',
        'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

        'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
        'TOKEN_TYPE_CLAIM': 'token_type',
        'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

        'JTI_CLAIM': 'jti',

        'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
        'SLIDING_TOKEN_LIFETIME': timedelta(minutes=int(os.environ.get('JWT_SLIDING_TOKEN_LIFETIME'))),
        'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=int(os.environ.get('JWT_SLIDING_TOKEN_REFRESH_LIFETIME'))),

        'SIGNING_KEY': os.environ.get("DJANGO_SECRET_KEY"),
    }

    # https://docs.djangoproject.com/en/4.1/ref/settings/#atomic-requests
    ATOMIC_REQUESTS = True
