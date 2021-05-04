"""
Django settings for pisti project.

Generated by 'django-admin startproject' using Django 3.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'tky^ogdw$1^87z_!u!!!e-z@$gr#61!+)levm)v5s_@95ioi6d'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['159.65.167.195', 'pisti.vishnu-pm.xyz']


# Application definition

INSTALLED_APPS = [
    'social_django',
    'user.apps.UserConfig',
    'adminapp.apps.AdminappConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'channels',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
]

ROOT_URLCONF = 'pisti.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')], 
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

AUTHENTICATION_BACKENDS = (
    'social_core.backends.facebook.FacebookOAuth2',
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.linkedin.LinkedinOAuth2',
    
    'django.contrib.auth.backends.ModelBackend',
)

WSGI_APPLICATION = 'pisti.wsgi.application'

DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'pisti',
        'USER': 'pistiuser',
        'PASSWORD': 'pistipass',
        'HOST': 'localhost',
        'PORT': '',
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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

AUTH_USER_MODEL = 'user.CustomUser'

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


GEOIP_PATH = os.path.join(BASE_DIR,'geoip')

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR,'static')
]
STATIC_ROOT = os.path.join(BASE_DIR,'assets')

MEDIA_ROOT = os.path.join(BASE_DIR,'static/media/')
MEDIA_URL = '/media/'

# chat settings
ASGI_APPLICATION = "pisti.routing.application"
CHANNEL_LAYERS = {
    "default": {
        "BACKEND":"channels.layers.InMemoryChannelLayer"
    }
}



LOGIN_REDIRECT_URL = '/user-home/'

SOCIAL_AUTH_FACEBOOK_KEY = '458153632283454' 
SOCIAL_AUTH_FACEBOOK_SECRET = 'b0ab837d508f6b08b4ee33bba115f5d5'

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '1028771307201-a23bn6l3o2te2tej1ve1tng34cb7alsu.apps.googleusercontent.com' 
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'xs6YZ5Cqtac-HKtcxmcG7tub'

SOCIAL_AUTH_LINKEDIN_OAUTH2_KEY = '86bu3mqlbxyt6f' 
SOCIAL_AUTH_LINKEDIN_OAUTH2_SECRET = 'ONAAaf4SaaxI5OEh'