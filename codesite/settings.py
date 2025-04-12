#Asetukset, lisähuomautukset tiedoston lopussa.
import os
from pathlib import Path
from datetime import timedelta
import sys
from pathlib import Path
from dotenv import load_dotenv
import mimetypes
mimetypes.add_type("text/css", ".css", True)

#käytetään dotenv tiedostoa tuomaan sensitiivistä dataa. 
#dotenv ei pushata git repoon

# Haetaan projektin juuri
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Määritellään .env-tiedoston polku ja ladataan se
# ENV_PATH = os.path.join(BASE_DIR, ".env")
# load_dotenv(ENV_PATH)

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
if "test" in sys.argv:
    # Testejä ajetaan → käytetään erillistä testisalasanaa
    SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "test-key-12345")
else:
    # Normaalikäyttö tai deploy → käytetään fallbackia jos SECRET_KEY puuttuu
    SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "fallback-key-for-ci")

    if SECRET_KEY == "fallback-key-for-ci":
        print("⚠️ Warning: SECRET_KEY not found in environment! Using fallback value.")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG") == "True"


# SECURITY WARNING: In production, allow only those domains which you trust.
#REST CORS ja sallitut domainit
# ALLOWED_HOSTS = [
#     'localhost', 
#     '127.0.0.1',
#     'codesitebe-efgshggehucfdvhq.swedencentral-01.azurewebsites.net',
#     'blue-wave-09f686903.6.azurestaticapps.net'
#     ]  #muutetttu * ---> tarkemmat määritykset

ALLOWED_HOSTS = ['*']

# #jos CAC == True niin tulee olla määritetyt originit ?
CORS_ALLOW_ALL_ORIGINS = True

# CORS_ALLOWED_ORIGINS = [
#     "http://localhost:5173",
#      "https://codesitebe-efgshggehucfdvhq.swedencentral-01.azurewebsites.net",
#      "https://blue-wave-09f686903.6.azurestaticapps.net"
#  ]

CORS_ALLOW_CREDENTIALS = True

# Application definition

INSTALLED_APPS = [
    'corsheaders',
    'rest_framework_simplejwt.token_blacklist',
    'rest_framework_simplejwt',
    'rest_framework',
    'codesitemainapp',
    'codesite',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
     "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'codesite.urls'

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

WSGI_APPLICATION = 'codesite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'mssql',
        'NAME': os.getenv("DATABASE_NAME"),
        'HOST': os.getenv("DATABASE_HOST"),
        'USER': os.getenv("DATABASE_USER"),
        'PASSWORD': os.getenv("DATABASE_PASSWORD"),
        'PORT': os.getenv("DATABASE_PORT"),
        'OPTIONS': {
	            'driver': 'ODBC Driver 17 for SQL Server',
	        },
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/
# Muutettu eurooppa/ suomi aika alueelle.
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Helsinki'

USE_I18N = True

# muuta tämä arvoon False jos aika alueet ei toimi(debug) TZ = timezone
USE_TZ = True



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'codesitemainapp.CustomUser'

REST_FRAMEWORK = {

    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication', #jos ei tarvita csrf tokenia
        'codesitemainapp.authentication.CookieJWTAuthentication'
    )

}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
}



#salasanan palautus

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv("EMAIL")
EMAIL_HOST_PASSWORD = os.getenv("EM_PASSWORD")


# Authentication
AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.ModelBackend']
# Käytetään SQLitea testauksen aikana, jotta vältetään SQL Serverin token_id -ongelmat,  Valter Backström 
import sys
if 'test' in sys.argv:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    }