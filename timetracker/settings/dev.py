from .base import *  # noqa

DEBUG = True

SECRET_KEY = 'CHANGEME!!!'

ALLOWED_HOSTS = ['*']

INTERNAL_IPS = ('127.0.0.1', '10.0.2.2')

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

CELERY_BROKER_URL = 'redis:///5'

SECURE_SSL_REDIRECT = False
