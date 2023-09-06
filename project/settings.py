"""
Django settings for project project.

Generated by 'django-admin startproject' using Django 4.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import os
from datetime import timedelta
from pathlib import Path

# settings.py

from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.


# remainder of file...

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-vyt=uc&i!e+u@kukacz8bz2r&$3dsc*ao$nq4pg#ot6iw4m)2&'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

CORS_ALLOW_CREDENTIALS = True


# settings.py

ALLOWED_HOSTS = ['p8081-z71384fb9-zd99dd61d-gtw.z503fe5f4.scsi.sh','*']

CSRF_TRUSTED_ORIGINS = [
    'https://p8081-z71384fb9-zd99dd61d-gtw.z503fe5f4.scsi.sh',
]

# Add your development machine IP address and iPhone IP address

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'drf_yasg',
    'custom_user',
    'registration',
    'Cities',
    'teamMembers',
    'bookmark',
    'Translation',
]

AUTH_USER_MODEL = 'custom_user.User'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # only once
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


CORS_ALLOWED_ORIGINS = [
    'http://localhost:*',  # Replace with your Expo Go URL
    'exp://127.0.0.1:*',
    'https://p8081-z71384fb9-zd99dd61d-gtw.z503fe5f4.scsi.sh'
]

ROOT_URLCONF = 'project.urls'

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

WSGI_APPLICATION = 'project.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('QOVERY_POSTGRESQL_Z8F433F1D_DEFAULT_DATABASE_NAME','postgres'),
        'USER': os.environ.get('QOVERY_POSTGRESQL_Z8F433F1D_LOGIN','qoveryadmin'),
        'PASSWORD': os.environ.get('QOVERY_POSTGRESQL_Z8F433F1D_PASSWORD'),
        'HOST': os.environ.get('QOVERY_POSTGRESQL_Z8F433F1D_HOST','z8f433f1d-postgresql.csihvcuphgw1.eu-central-1.rds.amazonaws.com'),
        'PORT': os.environ.get('QOVERY_POSTGRESQL_Z8F433F1D_PORT',5432)
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Authentication
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',

    ),
    # 'DEFAULT_PERMISSION_CLASSES': (
    #     'rest_framework.permissions.IsAuthenticated',
    # )
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=2),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=2)
}
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

