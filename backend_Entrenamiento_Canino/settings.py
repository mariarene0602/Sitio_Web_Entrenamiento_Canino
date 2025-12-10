# backend_Entrenamiento_Canino/settings.py

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-clave-secreta-aqui'

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app_Entrenamiento_Canino',
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

ROOT_URLCONF = 'backend_Entrenamiento_Canino.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'app_Entrenamiento_Canino', 'templates'),
        ],
        'APP_DIRS': True,  # Django automáticamente usa los loaders correctos
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

WSGI_APPLICATION = 'backend_Entrenamiento_Canino.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ==================== CONFIGURACIÓN DE EMAIL ====================
# PARA DESARROLLO: Emails se muestran en consola
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# PARA PRODUCCIÓN (CUANDO LO SUBAS A INTERNET):
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'tu_email@gmail.com'
# EMAIL_HOST_PASSWORD = 'contraseña_de_app'  # Usa contraseña de aplicación
# DEFAULT_FROM_EMAIL = 'CANIS Academia <info@canisacademia.com>'

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

LANGUAGE_CODE = 'es-mx'
TIME_ZONE = 'America/Mexico_City'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'app_Entrenamiento_Canino/static'),
]
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configuración de login/logout
LOGIN_URL = '/login/'  # Esta es la que falta
LOGIN_REDIRECT_URL = '/perfil/'
LOGOUT_REDIRECT_URL = '/'

SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Configuración de login/logout
LOGIN_URL = '/admin/login/'  # Para el admin Django
LOGIN_REDIRECT_URL = '/admin_dashboard/'  # Redirigir al dashboard después del login
LOGOUT_REDIRECT_URL = '/'

# Para superusuarios del Django Admin
ADMIN_LOGIN_REDIRECT_URL = '/admin_dashboard/'
