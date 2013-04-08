from .base import *

DATABASES = {
    'default': {
        'NAME': 'pentagon',
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'HOST': 'localhost',
        'USER': 'pentagon',
        'PASSWORD': 'somepassword',
    }
}

SECRET_KEY = 'not-so-secret'
PENTAGON_URL = 'http://localhost:8000'
