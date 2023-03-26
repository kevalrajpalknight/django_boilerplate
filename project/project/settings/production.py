import os
from .common import Common


class Production(Common):
    INSTALLED_APPS = Common.INSTALLED_APPS

    # https://docs.djangoproject.com/en/2.0/ref/settings/#allowed-hosts
    ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS').split(",")
    INSTALLED_APPS += ("gunicorn",)

    CORS_ORIGIN_WHITELIST = os.environ.get('CORS_ORIGIN_WHITELIST').split(",")
