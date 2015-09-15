from base import *
 
DEBUG = True
TEMPLATE_DEBUG = DEBUG
 
USE_LOCKSMITH = False
 
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(os.path.dirname(__file__), 'openstates.sqlite3'),
    }
}
