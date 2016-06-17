"""
Django settings for newsline project.

Generated by 'django-admin startproject' using Django 1.9.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NEWSLINE_DIR = BASE_DIR + "/newsline"

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'vjamef+8hj4ym-*h!f3t*7**%8&w!fw6oi!qzk0jd-eufja^5@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'newsline.apps.utility.logger',
    'newsline.apps.web.newsworm'
]

NEWSWORM_APPLICATION = 'newsline.apps.web.newsworm'

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'newsline.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'newsline.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default':{
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'newsline_failure_db',
        'USER': 'newsline_db_root',
        'PASSWORD': 'simple_root_pw',
        'HOST': '', # An empty string means localhost
        'PORT': '', # An empty string means the default port
    },

    'newsline_main_db': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'newsline_main_db',
        'USER': 'newsline_db_root',
        'PASSWORD': 'simple_root_pw',
        'HOST': '', # An empty string means localhost
        'PORT': '', # An empty string means the default port
    },

    'newsworm_db': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'newsline_newsworm',
        'USER': 'newsline_db_root',
        'PASSWORD': 'simple_root_pw',
        'HOST': '', # An empty string means localhost
        'PORT': '', # An empty string means the default port
    }
}

# This list contains the router for each application that this project owns.
# the order in which the routers are specified is significant.
# the newsworm database router is processed first, unless the models aren't those of his, other routers will proceed.

DATABASE_ROUTERS = ['newsline.apps.web.newsworm.database.database_router.NewswormDatabaseRouter','newsline.scripts.database_router.MainDatabaseRouter']

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'

# This indicates if the app is in test mode
import sys

TESTING = sys.argv[1:2] == ['test']

# The logging application and log files storage path
LOG_FILES_STORAGE = NEWSLINE_DIR + "/logs"
