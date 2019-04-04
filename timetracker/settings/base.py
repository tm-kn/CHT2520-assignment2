import os

import dj_database_url

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

    'timetracker.activities',
    'timetracker.projects',
    'timetracker.sheets.apps.SheetsConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
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

LOGIN_REDIRECT_URL = 'activities:list'

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

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
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
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': False,
        },
        'django.security': {
            'handlers': ['console'],
            'level': 'WARNING',
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

    AWS_S3_FILE_OVERWRITE = False

    AWS_S3_URL_PROTOCOL = os.environ.get('AWS_S3_URL_PROTOCOL', 'https:')

if 'CELERY_BROKER_URL' in os.environ:
    CELERY_BROKER_URL = os.environ['CELERY_BROKER_URL']

if 'BASE_URL' in os.environ:
    BASE_URL = os.environ['BASE_URL']
