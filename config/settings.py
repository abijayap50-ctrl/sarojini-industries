import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-sarojini-welding-showcase-open-source-2026')

DEBUG = os.environ.get('DEBUG', 'False').lower() in ('true', '1')

allowed_hosts_env = os.environ.get('ALLOWED_HOSTS', '')
if allowed_hosts_env:
    ALLOWED_HOSTS = [h.strip() for h in allowed_hosts_env.split(',') if h.strip()]
    if '*' not in ALLOWED_HOSTS and '.onrender.com' not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append('.onrender.com')
else:
    ALLOWED_HOSTS = ['*']

CSRF_TRUSTED_ORIGINS = [
    'https://*.onrender.com',
    'https://*.pythonanywhere.com',
    'http://localhost:8000',
    'http://127.0.0.1:8000',
]
extra_origins = os.environ.get('CSRF_TRUSTED_ORIGINS')
if extra_origins:
    CSRF_TRUSTED_ORIGINS.extend([o.strip() for o in extra_origins.split(',') if o.strip()])

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Showcase app
    'apps.showcase.apps.ShowcaseConfig',
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

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'config.wsgi.application'

import dj_database_url

DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

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

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

CLOUDINARY_URL = os.environ.get('CLOUDINARY_URL')
if CLOUDINARY_URL:
    CLOUDINARY_URL = CLOUDINARY_URL.strip().strip('"').strip("'")
    if 'cloudinary://' in CLOUDINARY_URL:
        CLOUDINARY_URL = 'cloudinary://' + CLOUDINARY_URL.split('cloudinary://', 1)[1].strip().strip('"').strip("'")
        os.environ['CLOUDINARY_URL'] = CLOUDINARY_URL

    if CLOUDINARY_URL.startswith('cloudinary://'):
        if 'cloudinary_storage' not in INSTALLED_APPS:
            idx = INSTALLED_APPS.index('django.contrib.staticfiles')
            INSTALLED_APPS.insert(idx, 'cloudinary_storage')
            INSTALLED_APPS.append('cloudinary')

        STORAGES = {
            "default": {
                "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
            },
            "staticfiles": {
                "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
            },
        }
        CLOUDINARY_STORAGE = {
            'CLOUDINARY_URL': CLOUDINARY_URL,
        }
    else:
        STORAGES = {
            "default": {
                "BACKEND": "django.core.files.storage.FileSystemStorage",
            },
            "staticfiles": {
                "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
            },
        }
else:
    STORAGES = {
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
        },
    }

WHITENOISE_MANIFEST_STRICT = False
WHITENOISE_USE_FINDERS = True

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
