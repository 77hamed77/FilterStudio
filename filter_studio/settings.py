"""""
Django settings for filter_studio project.
"""

from pathlib import Path
import os
import posixpath
from decouple import config, Csv
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)

default_host = 'filterstudio.onrender.com'
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default=default_host, cast=Csv())
if DEBUG:
    ALLOWED_HOSTS += ['127.0.0.1', 'localhost']

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'studio.apps.StudioConfig',
    'storages',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'filter_studio.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'filter_studio.wsgi.application'

# Database
DATABASE_URL = config('EXTERNAL_DATABASE_URL')
DATABASES = {
    'default': dj_database_url.parse(DATABASE_URL)
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    { 'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator' },
    { 'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator' },
    { 'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator' },
    { 'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator' },
]

# Internationalization
LANGUAGE_CODE = 'ar'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = 'static/'
STATIC_ROOT = posixpath.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [posixpath.join(BASE_DIR, 'static')]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files - Supabase S3 Compatible Storage Settings
AWS_ACCESS_KEY_ID = config('SUPABASE_S3_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('SUPABASE_S3_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = config('SUPABASE_S3_BUCKET_NAME')
AWS_S3_ENDPOINT_URL = config('SUPABASE_S3_ENDPOINT_URL')
AWS_S3_REGION_NAME = config('SUPABASE_S3_REGION_NAME')
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
AWS_S3_SIGNATURE_VERSION = 's3v4'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

MEDIA_URL = '/media/'
MEDIA_ROOT = posixpath.join(BASE_DIR, 'mediafiles')

# Authentication
LOGIN_URL = 'login/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

print("DEBUG:", DEBUG)
print("ALLOWED_HOSTS:", ALLOWED_HOSTS)
# أضف هذا السطر مع باقي الإعدادات الأمنية
CSRF_TRUSTED_ORIGINS = ['https://filterstudio.onrender.com']