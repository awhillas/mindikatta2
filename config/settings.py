"""
Django settings for mindikatta project.

Generated by 'django-admin startproject' using Django 1.10.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "mindikatta", "static"),
]

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'l(t((fr6q=u9#ifq5vm8tt5(*)q5rlgle2n(na4uo5(5#4*hxp'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DJANGO_DEBUG', True)

WSGI_APPLICATION = 'config.wsgi.application'

ALLOWED_HOSTS = []

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

FIXTURE_DIRS = ("mindikatta/harvest/fixtures/",)

# The weight to mulitipuly the counter by to get the weight of a counter weighing
HARVEST_WEIGHT_PER_COUNT = 25

# Application definition

INSTALLED_APPS = [
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'django.contrib.humanize',
	
	# 3rd party apps
	
	'django_extensions',
	'django_nose',
	
	
	# project apps
	
	'mindikatta.harvest',
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

ROOT_URLCONF = 'mindikatta.urls'

TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': ["mindikatta/templates"],
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

WSGI_APPLICATION = 'mindikatta.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
	}
}


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

# AUTH_PASSWORD_VALIDATORS = [
# 	{
# 		'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
# 	},
# 	{
# 		'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
# 	},
# 	{
# 		'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
# 	},
# 	{
# 		'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
# 	},
# ]

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Australia/Sydney'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Crispy forms

INSTALLED_APPS += ['crispy_forms']
CRISPY_TEMPLATE_PACK = 'bootstrap4'