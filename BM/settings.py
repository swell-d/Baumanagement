"""
Django settings for BM project.

Generated by 'django-admin startproject' using Django 4.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import os
from pathlib import Path

from django.contrib.messages import constants as messages
from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-*-(p%h@%zw*p$m(&fytg5gyv3q5-&qdo$jb0jkwch=cx(!cbwm'

# SECURITY WARNING: don't run with debug turned on in production!
# SWELL
if os.environ.get('DEBUG') == 'false':
    DEBUG = False
    ALLOWED_HOSTS = ['.herokuapp.com']
    # STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
    SECRET_KEY = '@xahLmB+g_^gVDbxKSR^njDT7=Y=+NKuK9BE^^a4T$M67Ec8Nu'
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': ('%(asctime)s [%(process)d] [%(levelname)s] ' +
                           'pathname=%(pathname)s lineno=%(lineno)s ' +
                           'funcname=%(funcName)s %(message)s'),
                'datefmt': '%Y-%m-%d %H:%M:%S'
            },
            'simple': {
                'format': '%(levelname)s %(message)s'
            }
        },
        'handlers': {
            'null': {
                'level': 'DEBUG',
                'class': 'logging.NullHandler',
            },
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'verbose'
            }
        },
        'loggers': {
            'testlogger': {
                'handlers': ['console'],
                'level': 'INFO',
            }
        }
    }
    DEBUG_PROPAGATE_EXCEPTIONS = True
else:
    DEBUG = True
    ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'author',
    'crispy_forms',
    'crispy_bootstrap5',
    'bootstrap5',
    'django_tables2',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Baumanagement.apps.BaumanagementConfig',
]

MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'author.middlewares.AuthorDefaultBackendMiddleware',
]

ROOT_URLCONF = 'BM.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'), 'Baumanagement/templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'BM.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

if 'RUN_IN_HEROKU' in os.environ:
    import django_heroku

    django_heroku.settings(locals())
    SECURE_HSTS_SECONDS = True
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'de'

TIME_ZONE = 'Europe/Berlin'

USE_I18N = True
USE_L10N = True
USE_TZ = True

LANGUAGES = (
    ('de', _('Deutsch')),
    ('en', _('English')),
)

LOCALE_PATHS = [
    os.path.join(BASE_DIR, "locale"),
    os.path.join(BASE_DIR, "Baumanagement/locale"),
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# SWELL
CSRF_TRUSTED_ORIGINS = ['https://*.herokuapp.com', 'http://127.0.0.1']
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

MESSAGE_TAGS = {
    messages.DEBUG: 'alert-warning',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
