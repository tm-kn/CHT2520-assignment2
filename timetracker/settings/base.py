import os

import dj_database_url
import raven
from raven.exceptions import InvalidGitRepository

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BASE_DIR = os.path.dirname(PROJECT_DIR)

DEBUG = False

if 'SECRET_KEY' in os.environ:
    SECRET_KEY = os.environ['SECRET_KEY']

if 'ALLOWED_HOSTS' in os.environ:
    ALLOWED_HOSTS = os.environ['ALLOWED_HOSTS'].split(',')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'django.contrib.sites',

    'rest_framework',

    'timetracker.accounts',
    'timetracker.activities',
    'timetracker.api',
    'timetracker.projects',
    'timetracker.sheets.apps.SheetsConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django_referrer_policy.middleware.ReferrerPolicyMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sites.middleware.CurrentSiteMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.RemoteUserMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'timetracker.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(PROJECT_DIR, 'templates'),
        ],
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

WSGI_APPLICATION = 'timetracker.wsgi.application'

DATABASES = {'default': dj_database_url.config(conn_max_age=600)}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME':
        'django.contrib.auth.password_validation.'
        'UserAttributeSimilarityValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LOGIN_REDIRECT_URL = 'home'

LANGUAGE_CODE = 'en-gb'

TIME_ZONE = 'Europe/London'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_ROOT = os.environ.get('STATIC_DIR', os.path.join(BASE_DIR, 'static'))

STATIC_URL = os.environ.get('STATIC_URL', '/static/')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static_compiled'),
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_ROOT = os.environ.get('MEDIA_DIR', os.path.join(BASE_DIR, 'media'))

MEDIA_URL = os.environ.get('MEDIA_URL', '/media/')

if os.environ.get('SECURE_SSL_REDIRECT', 'true').strip().lower() == 'true':
    SECURE_SSL_REDIRECT = True

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

if 'SECURE_HSTS_SECONDS' in os.environ:
    SECURE_HSTS_SECONDS = int(os.environ['SECURE_HSTS_SECONDS'])

if os.environ.get('SECURE_BROWSER_XSS_FILTER',
                  'true').lower().strip() == 'true':
    SECURE_BROWSER_XSS_FILTER = True

if os.environ.get('SECURE_CONTENT_TYPE_NOSNIFF',
                  'true').lower().strip() == 'true':
    SECURE_CONTENT_TYPE_NOSNIFF = True

REFERRER_POLICY = os.environ.get('SECURE_REFERRER_POLICY',
                                 'strict-origin').strip()

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'sentry': {
            'level': 'ERROR',
            'class':
            'raven.contrib.django.raven_compat.handlers.SentryHandler',
        },
    },
    'formatters': {
        'verbose': {
            'format':
            '[%(asctime)s][%(process)d][%(levelname)s][%(name)s] %(message)s'
        }
    },
    'loggers': {
        'timetracker': {
            'handlers': ['console', 'sentry'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['console', 'sentry'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.security': {
            'handlers': ['console', 'sentry'],
            'level': 'WARNING',
            'propagate': False,
        },
        'django.security.DisallowedHost': {
            'handlers': ['console'],
            'propagate': False,
        },
    },
}

if os.environ.get('SECURE_SSL_REDIRECT', 'true').strip().lower() == 'true':
    SECURE_SSL_REDIRECT = True

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

if 'SECURE_HSTS_SECONDS' in os.environ:
    SECURE_HSTS_SECONDS = int(os.environ['SECURE_HSTS_SECONDS'])

if os.environ.get('SECURE_BROWSER_XSS_FILTER',
                  'true').lower().strip() == 'true':
    SECURE_BROWSER_XSS_FILTER = True

if os.environ.get('SECURE_CONTENT_TYPE_NOSNIFF',
                  'true').lower().strip() == 'true':
    SECURE_CONTENT_TYPE_NOSNIFF = True

if 'AWS_STORAGE_BUCKET_NAME' in os.environ:
    INSTALLED_APPS.append('storages')

    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

    AWS_STORAGE_BUCKET_NAME = os.environ['AWS_STORAGE_BUCKET_NAME']

    AWS_QUERYSTRING_AUTH = False

    AWS_DEFAULT_ACL = None

    AWS_S3_FILE_OVERWRITE = False

    AWS_QUERYSTRING_AUTH = True

    AWS_QUERYSTRING_EXPIRE = 120

    AWS_S3_URL_PROTOCOL = os.environ.get('AWS_S3_URL_PROTOCOL', 'https:')

    AWS_S3_SIGNATURE_VERSION = os.environ.get('AWS_S3_SIGNATURE_VERSION',
                                              's3v4')

    AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME')

if 'CELERY_BROKER_URL' in os.environ:
    CELERY_BROKER_URL = os.environ['CELERY_BROKER_URL']

if 'EMAIL_HOST' in os.environ:
    EMAIL_HOST = os.environ['EMAIL_HOST']

if 'EMAIL_PORT' in os.environ:
    try:
        EMAIL_PORT = int(os.environ['EMAIL_PORT'])
    except ValueError:
        pass

if 'EMAIL_HOST_USER' in os.environ:
    EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']

if 'EMAIL_HOST_PASSWORD' in os.environ:
    EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']

if os.environ.get('EMAIL_USE_TLS', 'false').lower().strip() == 'true':
    EMAIL_USE_TLS = True

if os.environ.get('EMAIL_USE_SSL', 'false').lower().strip() == 'true':
    EMAIL_USE_SSL = True

if 'EMAIL_SUBJECT_PREFIX' in os.environ:
    EMAIL_SUBJECT_PREFIX = os.environ['EMAIL_SUBJECT_PREFIX']

if 'SERVER_EMAIL' in os.environ:
    SERVER_EMAIL = DEFAULT_FROM_EMAIL = os.environ['SERVER_EMAIL']

if 'SENTRY_DSN' in os.environ:
    INSTALLED_APPS.append('raven.contrib.django.raven_compat')

    RAVEN_CONFIG = {
        'dsn': os.environ['SENTRY_DSN'],
        'tags': {},
    }

    RAVEN_CONFIG['tags']['lang'] = 'python'

    try:
        RAVEN_CONFIG['release'] = raven.fetch_git_sha(BASE_DIR)
    except InvalidGitRepository:
        pass

AUTH_USER_MODEL = 'accounts.User'

SITE_ID = 1
