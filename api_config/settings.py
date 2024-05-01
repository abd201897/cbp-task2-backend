"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 5.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
import os
from pathlib import Path
from datetime import timedelta
from decouple import config, Csv
from corsheaders.defaults import default_headers

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', cast=str)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', cast=bool)

WEBSITE_HOSTNAME = config('WEBSITE_HOSTNAME', default='*', cast=Csv())

if DEBUG:
    ALLOWED_HOSTS = ['*']

else:

    ALLOWED_HOSTS = [WEBSITE_HOSTNAME]

    CSRF_TRUSTED_ORIGINS = [f'https://{WEBSITE_HOSTNAME}']


CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = list(default_headers)
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Acure Blob Access Keys
AZURE_BLOB_KEY =  config('AZURE_BLOB_KEY', default='*', cast=str)
AZURE_BLOB_STORAGE_ACCOUNT = config('AZURE_BLOB_STORAGE_ACCOUNT', default='*', cast=str)
AZURE_BLOB_CONTAINER_NAME = config('AZURE_BLOB_CONTAINER_NAME', default='*', cast=str) 

# Application definition

CORE_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

CUSTOM_APPS = [
    'accounts.apps.AccountsConfig',
    'courses.apps.CoursesConfig',
    'utils.apps.UtilsConfig'
]

THIRD_PARTY_APPS = [
    'rest_framework_simplejwt.token_blacklist',
    'corsheaders',
    'django_extensions'
]

INSTALLED_APPS = CORE_APPS + CUSTOM_APPS + THIRD_PARTY_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'api_config.urls'
AUTH_USER_MODEL = "accounts.User"


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

WSGI_APPLICATION = 'api_config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('MYSQL_DB', cast=str),
        'USER': config('MYSQL_USER', cast=str),
        'PASSWORD': config('MYSQL_PASS', cast=str),
        'HOST': config('MYSQL_HOST', cast=str),
        'PORT': config('MYSQL_PORT', cast=str),
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
        'rest_framework.permissions.AllowAny',
        'rest_framework.permissions.IsAdminUser',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}


SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=8),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': config('JWT_TEKON', cast=str),
    'VERIFYING_KEY': config('JWT_TEKON', cast=str),

    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}



# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Configure email settings
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST', cast=str)  # SMTP server
EMAIL_PORT = config('EMAIL_PORT', cast=int)  # SMTP port
# EMAIL_USE_TLS = True  # TLS is required
EMAIL_HOST_USER = config('EMAIL_HOST_USER', cast=str)  # Your email address
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', cast=str)  # Your password or app-specific password
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', cast=str)  # The default sender email address (must be your email)


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/
STORAGES = {
    "default": {
        "BACKEND": "storages.backends.azure_storage.AzureStorage",
        "OPTIONS": {
            "account_name": AZURE_BLOB_STORAGE_ACCOUNT,
            "account_key": AZURE_BLOB_KEY,
            "azure_container": os.path.join(AZURE_BLOB_CONTAINER_NAME, 'media'),
        },
    },
    "staticfiles": {
        "BACKEND": "storages.backends.azure_storage.AzureStorage",
        "OPTIONS": {
            "account_name": AZURE_BLOB_STORAGE_ACCOUNT,
            "account_key": AZURE_BLOB_KEY,
            "azure_container": os.path.join(AZURE_BLOB_CONTAINER_NAME, 'static'),
        },
    },
}

STATIC_URL = f'https://{AZURE_BLOB_STORAGE_ACCOUNT}.blob.core.windows.net/{AZURE_BLOB_CONTAINER_NAME}/static/'

MEDIA_URL = f'https://{AZURE_BLOB_STORAGE_ACCOUNT}.blob.core.windows.net/{AZURE_BLOB_CONTAINER_NAME}/media/'


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
