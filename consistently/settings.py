"""
Django settings for consistently project.

Generated by 'django-admin startproject' using Django 2.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
import json
import consistently as project_module
from django.urls import reverse_lazy
import django_heroku
import dj_database_url

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = os.path.join(BASE_DIR, 'consistently')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'jqw!s7t7^88&enk)1bll$w8rx31yd6v7z01#0jw@2xn!1b*)+r'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', False)

ALLOWED_HOSTS = ['*', ]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'acme_challenge',
    'django_celery_results',
    'rest_framework',
    'social_django',

    'consistently',
    'consistently.apps.api',
    'consistently.apps.repos',
    'consistently.apps.integrations',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'consistently.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(PROJECT_DIR, 'templates'), ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'consistently.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases
# django_heroku doesn't quite handle this right
# https://github.com/heroku/django-heroku/issues/10

DATABASES = {
    'default': dj_database_url.parse(
        os.environ.get('DATABASE_URL', "sqlite:///db.sqlite3")),
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# ==============================================================================
# social-auth config
# ==============================================================================

AUTHENTICATION_BACKENDS = (
    'social_core.backends.github.GithubOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

# @todo - eventually request less scope initially (https://bit.ly/2DZzEeZ)

SOCIAL_AUTH_GITHUB_KEY = os.environ.get('GITHUB_KEY', None)
SOCIAL_AUTH_GITHUB_SECRET = os.environ.get('GITHUB_SECRET', None)
SOCIAL_AUTH_GITHUB_SCOPE = [
    'read:org',
    'admin:repo_hook', ]
SOCIAL_AUTH_LOGIN_REDIRECT_URL = reverse_lazy('repos:profile')

# github will need to be updated for dev environment
# https://github.com/settings/applications/677341

# When using postgres
SOCIAL_AUTH_POSTGRES_JSONFIELD = os.environ.get(
    'SOCIAL_AUTH_POSTGRES_JSONFIELD', False)

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication'
    ]
}

# ==============================================================================
# Local dev with React
# ==============================================================================

REACT_APP_NAME = 'react-app'

if DEBUG:
    MIDDLEWARE.append('consistently.dev_middleware.dev_cors_middleware')

REACT_BASE_DIR = os.path.join(BASE_DIR, REACT_APP_NAME)
REACT_BUILD_DIR = os.path.join(REACT_BASE_DIR, 'build')

STATICFILES_DIRS = [
    os.path.join(REACT_BUILD_DIR, 'static'),
    os.path.join(PROJECT_DIR, 'static')
]

# Pull the js and css filenames from the current build
path = os.path.join(REACT_BUILD_DIR, "asset-manifest.json")
with open(path) as f:
    data = json.load(f)

# REACT_CSS_PATH = data['main.css'].replace('static/', '')
REACT_CSS_PATH = None
REACT_JS_PATH = data['main.js'].replace('static/', '')

# ==============================================================================
# Github Webhook
# ==============================================================================

PUBLIC_URL = os.environ.get('PUBLIC_URL', 'http://consistently.io/')
WEBHOOK_URL = reverse_lazy('api:github-webhook')

# ==============================================================================
# Celery
# ==============================================================================

CELERY_BROKER_URL = os.environ.get(
    'REDIS_URL', 'amqp://guest:guest@localhost//')
CELERY_RESULT_BACKEND = os.environ.get('REDIS_URL', 'django-db')

CELERY_TASK_ALWAYS_EAGER = os.environ.get('CELERY_ALWAYS_EAGER', False)
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'

django_heroku.settings(locals(), databases=not DEBUG)
