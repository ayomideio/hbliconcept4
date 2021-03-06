"""
Django settings for book_testing project.

Generated by 'django-admin startproject' using Django 3.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""
# from django.utils.encoding import python_2_unicode_compatible
from . import apps
import os
import iconcept4.authRouter
import iconcept4.PrimaryReplicaRouter
# import ldap
# from django_auth_ldap.config import LDAPSearch

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '!q*l8^9-bjs$qr#o_q7kr9f)j!me3prpdsn8!g^bo(w8xg54na'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
SITE_ID = 1
ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'grappelli',    
    # 'filebrowser',
    # 'django.contrib.admin',
    # 'book_testing.book_testing.apps.BookConfig'
    'iconcept4.apps.BookConfig',
    'CheckComp.apps.CheckcompConfig',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    
    'calloverexceptionreview',
   
    'CalloverforControl',
    'pendingcalloverforcontrol',
    'calloverforcontrolspecial',
    'pendingcalloverforcontrolspecial',
    
    'manual_exception',
    
    'alert_review',
    
    # 'calloverexceptionreview',    
    'userapp',

    'allauth.socialaccount',
    'corsheaders'
    # 'module1.apps.Module1Config',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django_session_timeout.middleware.SessionTimeoutMiddleware',

    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]

ROOT_URLCONF = 'iconcept4.urls'

CORS_ORIGIN_ALLOW_ALL = True

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'), os.path.join(BASE_DIR, 'templates', 'allauth')],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': False,
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.media',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'iconcept4.wsgi.application'

AUTH_LDAP_SERVER_URI = "wema"
AUTH_LDAP_BIND_DN = "cn=admin,dc=example,dc=com"
AUTH_LDAP_BIND_PASSWORD = "test@1234"
# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

# DB setting for SQLite3

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

# DB setting for MSSQL server
DATABASES = {
    'default':{
        'NAME':      'orcl',
        'ENGINE': 'django.db.backends.oracle',
        'USER': 'u_ic4indep',
        'PASSWORD': 'c4',
        'HOST': 'localhost',
        'PORT': '1521',
    },  
    # 'auth_db':{
    #     'NAME': 'orcl',
    #     'ENGINE': 'django.db.backends.oracle',
    #     'USER': 'u_iconcept4',
    #     'PASSWORD': 'c4',
    #     'HOST': 'localhost',
    #     'PORT': '1521',
    # },
    #  'default': {
        
    #     'ENGINE': 'django.db.backends.oracle',
    #     'NAME': 'ubnx01-scan6:8732/iconcept4',
    #     'USER': 'U_IC4INDEP',
    #     'PASSWORD': 'c4'
    #  }

}


# DATABASE_ROUTERS = [book_testing.authRouter, book_testing.PrimaryReplicaRouter]

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

ROOT_URLCONF = 'iconcept4.urls'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'


ACCOUNT_FORMS = {
    'login': 'CheckComp.forms.CustomLoginForm',
    'signup': 'CheckComp.forms.CustomSignupForm',
}

EMAIL_BACKEND = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
    # 'django.core.mail.backends.smtp.EmailBackend'
)

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'adelekeluqman@gmail.com'
EMAIL_HOST_PASSWORD = 'sokedile.com'

ACCOUNT_AUTHENTICATION_METHOD ="username_email"
ACCOUNT_USERNAME_REQUIRED = True

LOGIN_URL = '/login'
LOGIN_REDIRECT_URL = '/home'
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_LOGOUT_REDIRECT_URL ="/login"


ADMIN_LOGIN_REDIRECT_URL = '/library/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

STATIC_ROOT=os.path.join(BASE_DIR,'static')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "iconcept4/static"),
]
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
# SESSION_COOKIE_AGE = 60*50 # set just 10 seconds to test
SESSION_SAVE_EVERY_REQUEST = True
SESSION_TIMEOUT_REDIRECT = '/login'
DATA_UPLOAD_MAX_NUMBER_FIELDS =780000000000