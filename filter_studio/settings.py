"""
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
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv(), default=[])
if DEBUG:
    ALLOWED_HOSTS += ['127.0.0.1', 'localhost']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'studio.apps.StudioConfig',
    'storages', # <-- ✅ إضافة django-storages
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
    { 'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]

# Internationalization
LANGUAGE_CODE = 'ar'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_ROOT = posixpath.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    posixpath.join(BASE_DIR, 'static'),
]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files - Supabase S3 Compatible Storage Settings
# ✅ هذا هو الجزء الجديد والمهم
AWS_ACCESS_KEY_ID = config('SUPABASE_S3_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('SUPABASE_S3_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = config('SUPABASE_S3_BUCKET_NAME')
AWS_S3_ENDPOINT_URL = config('SUPABASE_S3_ENDPOINT_URL')
AWS_S3_REGION_NAME = config('SUPABASE_S3_REGION_NAME')
# `AWS_S3_FILE_OVERWRITE` is a setting that controls whether files with the same name are allowed to
# be overwritten when uploading to the specified S3 bucket.
AWS_S3_FILE_OVERWRITE = False # لا تسمح بالكتابة فوق الملفات بنفس الاسم
AWS_DEFAULT_ACL = 'public-read' # لجعل الملفات المرفوعة قابلة للقراءة بشكل عام

# Set the default storage for media files
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

MEDIA_URL = '/media/'
# MEDIA_ROOT لم يعد ضرورياً بنفس القدر عندما يتم الرفع مباشرة إلى S3
# ولكن لا بأس من الاحتفاظ به كـ fallback أو لتوضيح المسار المحلي
MEDIA_ROOT = posixpath.join(BASE_DIR, 'mediafiles')

# Authentication settings
LOGIN_URL = 'login/'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'