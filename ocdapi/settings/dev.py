from .base import *

SECRET_KEY = 'not-so-secret'

DATABASES = {
    'default': {
        'NAME': 'api',
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'HOST': 'localhost',
        'USER': 'api',
        'PASSWORD': 'test',
    }
}

ALLOWED_HOSTS = [
    '127.0.0.1', 'localhost',
]

DEBUG=True
