import environ
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, "subdir").
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/
env = environ.Env(
    DEBUG=(bool, False)
)
environ.Env.read_env()

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG")

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    # local packages
    "cart.apps.CartConfig",
    "shop.apps.ShopConfig",
    "payments.apps.PaymentsConfig",

    # built-in packages
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',

    # third part packages
    "ckeditor",
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

ROOT_URLCONF = 'core.urls'

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
                "shop.context_processors.shop",
                "shop.context_processors.shop_form",
                "cart.context_processors.cart",
            ],
        },
    },
]

# Authentication backends with custom backend called EmailAuthBackend
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "auth.authentication.EmailAuthBackend",
]

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env("NAME"),
        'USER': env("PSQL_USER"),
        'PASSWORD': env("PASSWORD"),
        'HOST': env("HOST"),
        'PORT': env("PORT"),
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Samarkand'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, "static_root")

STATICFILES_DIRS = [
    os.path.join("static"),
]

MEDIA_URL = "/media/"

MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MESSAGE_STORAGE = "django.contrib.messages.storage.cookie.CookieStorage"

EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ.get("email")
EMAIL_HOST_PASSWORD = os.environ.get("email_password")
EMAIL_USE_TLS = True

STRIPE_SECRET_KEY = "sk_test_51O4Sg5CKkMgPTgjF873npoysptsBe6XjMKfMPLnWxtOEeuOQWlgvl6ICmEXRRM5Ryq935o8MyuB0VXG0i0OOUSDm00JRufk6Cd"
STRIPE_PUBLIC_KEY = "pk_test_51O4Sg5CKkMgPTgjFYEPduL4au2zwLEfIBk9OvOzjCz5BkEZ3PCSDmSVkzfszbMuLihPoHqiqoiOP5AV91ljwhmXY00KBUmRFak"
STRIPE_API_VERSION = "2023-10-16"

CART_SESSION_ID = "cart"

LOGIN_URL = "auth:login"

STRIPE_WEBHOOK_SECRET = "whsec_4b4397bbea52daa6b297bb98bde154db210e6b95d3f716bfb04f21e5944a5350"
