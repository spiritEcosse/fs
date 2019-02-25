"""
Django settings for fs project.

Generated by 'django-admin startproject' using Django 1.8.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from django.utils.translation import ugettext_lazy as _
import dj_database_url

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '4w+so4bufn#8855(e+23(=si*^i&hf60z&v+2=-*qu_1rw+i)b'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'haystack',
    'materials',
    'comments',
    'search',
    'debug_toolbar',
    'multiselectfield',
    'goslate',
    'djangular',
    'ex_user',
    'crispy_forms',
    'tastypie',
)

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(os.path.dirname(__file__), 'whoosh_index'),
    },
}

# HAYSTACK_CONNECTIONS = {
#     'default': {
#         'ENGINE':
#         'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
#         'URL':
#         'http://elasticsearch:9200/',
#         'INDEX_NAME':
#     },
# }

TEMPLATE_CONTEXT_PROCESSORS = ('django.template.context_processors.request', )

MIDDLEWARE_CLASSES = (
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.locale.LocaleMiddleware',
)

ROOT_URLCONF = 'fs.urls'

LOCALE_PATHS = (os.path.join(BASE_DIR, 'locale'), )

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'fs.template.context_processors.context_data',
            ],
        },
    },
]

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

WSGI_APPLICATION = 'fs.wsgi.application'
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/profile/'

DATABASES = {
    'default': {
        'ENGINE':
        'django.db.backends.postgresql_psycopg2',
        'NAME':
        'd8ng184nhikr6',
        'USER':
        'fkftotqckdvtug',
        'PASSWORD':
        '55e6873e1d70daadc9ea832a7e82621da3e03e0c783ccf1832e2d9192d9b2e7f',
        'HOST':
        'ec2-23-21-165-188.compute-1.amazonaws.com',
        'PORT':
        '5432',
    }
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'fs',
        'USER': 'fs',
        'PASSWORD': 'fs',
        'HOST': 'db',
        'PORT': '',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Kiev'

USE_I18N = True

USE_L10N = True

USE_TZ = True

USE_THOUSAND_SEPARATOR = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static_root')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = "/media/"

STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'), )

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

TEMPLATE_DIRS = (os.path.join(BASE_DIR, 'templates'), )

CRISPY_TEMPLATE_PACK = 'bootstrap'
DEFAULT_FROM_EMAIL = 'shevchenkcoigor@gmail.com'

LANGUAGES = (
    (
        'ru',
        _('Russia'),
    ),
    ('en', _('English')),
)

CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']

if os.environ.get('PRODUCTION', False):
    REDIS_URL = os.environ.get("REDIS_URL")

    # DEBUG = False
    DATABASES['default'] = dj_database_url.config(
        default=os.environ.get('DATABASE_URL'))
else:
    REDIS_URL = 'redis://redis:6379/1'

raise Exception(os.environ.get("REDIS_URL"))
CACHES = {
    "default": {
        "BACKEND": "redis_cache.RedisCache",
        "LOCATION": REDIS_URL,
    }
}

CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL
CELERY_TIMEZONE = TIME_ZONE
