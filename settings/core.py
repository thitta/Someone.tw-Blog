import importlib
import os

from django.urls import reverse_lazy

# ---------- get env variable ----------

USE_PROD_CFG = True if os.getenv("SOMEONE_USE_PROD_CFG", None) == "TRUE" else False
USE_PROD_DB = True if os.getenv("SOMEONE_USE_PROD_DB", None) == "TRUE" else False

# ---------- import settings ----------

PACKAGE = "settings.django_settings"

site_setting = importlib.import_module(name=".cfg_dev", package=PACKAGE)
db_setting = importlib.import_module(name=".db_dev", package=PACKAGE)

if USE_PROD_DB is True:
    site_setting = importlib.import_module(name=".db_prod", package=PACKAGE)

if USE_PROD_CFG is True:
    db_setting = importlib.import_module(name=".cfg_prod", package=PACKAGE)

# ---------- DJANGO CORE ---------
ALLOWED_HOSTS = site_setting.ALLOWED_HOSTS
DEBUG = site_setting.DEBUG

# ---------- DATABASE ----------
DATABASES = db_setting.DATABASES
CONN_MAX_AGE = db_setting.CONN_MAX_AGE

# ---------- SITE STATIC ----------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = site_setting.STATIC_URL

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'sn6lx$e^*$7*16j^%sjv8(3+0_c2kwqx#zfhqzs8*!7gz2h*_i'

# Application definition
AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.ModelBackend']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "cms.apps.CmsConfig",
    "settings"
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

ROOT_URLCONF = 'someone_blog.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'someone_blog.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

# en-us, ah-hant
LANGUAGE_CODE = 'en-us'

# 'America/Chicago', Asia/Taipei
TIME_ZONE = 'Asia/Taipei'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOGIN_REDIRECT_URL = "cms_post_list_url"
LOGOUT_REDIRECT_URL = "cms_post_list_url"
LOGIN_URL = reverse_lazy("cms_post_list_url")
