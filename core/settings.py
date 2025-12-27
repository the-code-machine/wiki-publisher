from pathlib import Path
import os
from dotenv import load_dotenv
import dj_database_url

# 1. FIX: Only define BASE_DIR once
BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env file (for local development)
load_dotenv(BASE_DIR / ".env")

# 2. FIX: Smart DEBUG switching
# If we are on Render, DEBUG should be False. Locally, it defaults to True.
# We check if the 'RENDER' environment variable exists.
DEBUG = 'RENDER' not in os.environ

# SECURITY WARNING: keep the secret key used in production secret!
# On Render, set a SECRET_KEY environment variable. Fallback is for dev only.
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-)*cje2+d-h_u9oxtb1^$^2xra)fcna=+8i5yv!blumff-^i8t0')

ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    "jazzmin",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # MY APP
    'publisher',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware", # <--- CORRECT LOCATION
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls' # Ensure your main folder is actually named 'core'. If it is 'config', change this to 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'core.wsgi.application' # Same here: check if folder is 'core' or 'config'

# Database
# Uses DATABASE_URL from Render if available, otherwise uses local sqlite
DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3'),
        conn_max_age=600
    )
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    { 'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Jazzmin Settings
JAZZMIN_SETTINGS = {
    "site_title": "Core Admin",
    "site_header": "Core Admin",
    "site_brand": "Core",
    "welcome_sign": "Welcome to Core Admin",
    "theme": "darkly",
}

# --- STATIC FILES CONFIGURATION (FIXED) ---
# This setup works for both Local (Dev) and Render (Prod) without changing code.

STATIC_URL = 'static/'

# 1. Always define STATIC_ROOT. This fixes "ImproperlyConfigured" errors on build.
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# 2. Only add STATICFILES_DIRS if the local folder actually exists.
# This prevents the "directory does not exist" warning.
local_static_dir = os.path.join(BASE_DIR, 'static')
if os.path.exists(local_static_dir):
    STATICFILES_DIRS = [local_static_dir]

# 3. Enable WhiteNoise for serving files
# We use this storage engine which hashes files (good for caching)
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'