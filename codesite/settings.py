#Asetukset, lisä huomautukset tiedoston lopussa.
import os
from pathlib import Path
from datetime import timedelta

from pathlib import Path
from dotenv import load_dotenv
import mimetypes
mimetypes.add_type("text/css", ".css", True)

#käytetään dotenv tiedostoa tuomaan sensitiivistä dataa. 
#dotenv ei pushata git repoon
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG")

# SECURITY WARNING: In production, allow only those domains which you trust.
#REST CORS ja sallitut domainit
ALLOWED_HOSTS = [
    'localhost', 
    '127.0.0.1',
    'codesitebe-efgshggehucfdvhq.swedencentral-01.azurewebsites.net'
    ]  #muutetttu * ---> tarkemmat määritykset



#jos CAC == True niin tulee olla määritetyt originit
CSRF_TRUSTED_ORIGINS = ['https://*.azurewebsites.net',
                        'https://codesitebe-efgshggehucfdvhq.swedencentral-01.azurewebsites.net',     #azure täytyy olla
                        'http://localhost:3000']

#CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOWED_ORIGINS = [
   "http://localhost:5173",
    "https://codesitebe-efgshggehucfdvhq.swedencentral-01.azurewebsites.net",
]


CORS_ALLOW_CREDENTIALS = True


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'codesitemainapp',
    'rest_framework',
    'corsheaders',
    'codesite',
       
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',                 #paras yhteensopivuus kun ylimpänä
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
        'NAME': os.getenv("DB_NAME"),
        'HOST': os.getenv("DB_HOST"),
        'USER': os.getenv("DB_USER"),
        'PASSWORD': os.getenv("DB_PASS"),
        'PORT' : '1433',
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
# https://docs.djangoproject.com/en/4.0/howto/static-files/
# varmista polut
STATIC_URL = '/static/'
STATIC_ROOT = 'static'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'codesitemainapp.CustomUser'



#Autentikaatio asetukset tähän alle
#cookies
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'codesitemainapp.authentication.CookieJWTAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

#token jwt
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),  # Käyttäjän tokenin voimassaoloaika
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),     # Refresh-tokenin voimassaoloaika
    'ROTATE_REFRESH_TOKENS': True,                  # Luo uusi refresh-token käytettäessä
    'BLACKLIST_AFTER_ROTATION': True,               # Vanha refresh-token mitätöityy
    'AUTH_HEADER_TYPES': ('Bearer',),               # Käytä "Bearer" -headeria ei tarvita kun evästeet käytössä
    
    #lisätään muutama määritys 
    'AUTH_COOKIE': 'access_token',      # Evästeen nimi
    "AUTH_COOKIE_REFRESH": 'refresh',  # Refresh-token evästeessä
    'AUTH_COOKIE_HTTP_ONLY': True,      # Vain HTTP-käyttö (ei JS)
    'AUTH_COOKIE_SECURE': True,         # HTTPS-vaatimus
    'AUTH_COOKIE_SAMESITE': 'None',     # Tarvitaan, jos React pyytää cross-origin localhost ajossa vaihda 'Lax'
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",)
}   


#Autentikaatio asetus osion loppu

#Lisä asetukset 1 start CORS CSRF COOKIES  
CSRF_COOKIE_HTTPONLY = False  # Salli JavaScriptin käyttää CSRF-evästettä
CSRF_COOKIE_SECURE = True  # Pakottaa HTTPS-yhteyden (Azure)
CORS_ALLOW_CREDENTIALS = True  # Salli evästeet ja JWT-kirjautuminen
CSRF_COOKIE_SAMESITE = 'None'
#Lisä asetukset 1 end

#Lisä asetukset 2 start
SESSION_COOKIE_SAMESITE = 'None'  # Tarvitaan cross-origin-pyynnöissä
SESSION_COOKIE_SECURE = True  # Sama HTTPS-vaatimus sessioevästeille
#Lisä asetukset 2 end
