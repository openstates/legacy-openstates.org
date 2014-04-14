import os
import datetime
from django.core.exceptions import ImproperlyConfigured

def envvar(name, default=None):
    result = os.environ.get(name, default)
    if result is None:
        raise ImproperlyConfigured('missing required environment variable ' + name)
    return result

# env variables
SECRET_KEY = envvar('SECRET_KEY')
RAVEN_DSN = envvar('RAVEN_DSN', '')
ALLOWED_HOSTS = envvar('ALLOWED_HOSTS', '*').split(',')
DATABASE_NAME = envvar('DATABASE_NAME', 'api')
DATABASE_HOST = envvar('DATABASE_HOST', 'localhost')
DATABASE_USER = envvar('DATABASE_USER', 'api')
DATABASE_PASSWORD = envvar('DATABASE_NAME', 'api')
IMAGO_MONGO_URI = envvar('IMAGO_MONGO_URI', 'mongodb://localhost')
LOCKSMITH_MONGO_HOST = envvar('LOCKSMITH_MONGO_HOST', IMAGO_MONGO_URI)
ELASTICSEARCH_HOST = envvar('ELASTICSEARCH_HOST', 'http://localhost:9200')
TEMPLATE_DEBUG = DEBUG = envvar('DJANGO_DEBUG', 'False').lower() == 'true'
USE_LOCKSMITH = envvar('USE_LOCKSMITH', 'False').lower() == 'true'
if USE_LOCKSMITH:
    LOCKSMITH_SIGNING_KEY = envvar('LOCKSMITH_SIGNING_KEY')


# settings we don't override
TIME_ZONE = 'America/New_York'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = False
USE_L10N = False

MEDIA_ROOT = ''
MEDIA_URL = ''
STATIC_ROOT = ''
STATIC_URL = '/static/'
ADMIN_MEDIA_PREFIX = '/static/admin/'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'ocdapi.urls'

TEMPLATE_DIRS = (
    os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates')),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sites',
    'south',
    'boundaries',
    'imago',
)
if RAVEN_DSN:
    INSTALLED_APPS += ('raven.contrib.django.raven_compat',)
    RAVEN_CONFIG = {'dsn': RAVEN_DSN}

DATABASES = {
    'default': {
        'NAME': DATABASE_NAME,
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'HOST': DATABASE_HOST,
        'USER': DATABASE_USER,
        'PASSWORD': DATABASE_PASSWORD,
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'boundaries': {
             'handlers': ['console'],
             'level': 'INFO',
             'formatter': 'simple'
        },
    }
}

# locksmith stuff
if USE_LOCKSMITH:
    INSTALLED_APPS += ('locksmith.mongoauth',)
    MIDDLEWARE_CLASSES += ('locksmith.mongoauth.middleware.APIKeyMiddleware',)
    LOCKSMITH_REGISTRATION_URL = 'http://sunlightfoundation.com/api/accounts/register/#ocd'
    LOCKSMITH_HUB_URL = 'http://sunlightfoundation.com/api/analytics/'
    LOCKSMITH_API_NAME = 'opencivicdata'

BOUNDARIES_SHAPEFILES_DIR = 'shapefiles'
IMAGO_COUNTRY = 'us'
IMAGO_BOUNDARY_MAPPINGS = {
    'county-13': {'key': 'census_geoid',
                  'start': datetime.date(1980,1,1),
                  'prefix': 'place-',
                  'ignore': None,
                 },
    'place-13': {'key': 'census_geoid',
                 'start': datetime.date(1980,1,1),
                  'prefix': 'place-',
                 'ignore': '.*CDP',
                },
    'sldl-13': {'key': 'census_geoid',
                'start': datetime.date(2012,1,1),
                'prefix': 'sldl-',
                'ignore': '.*ZZZ',
               },
    'sldu-13': {'key': 'census_geoid',
                'start': datetime.date(2012,1,1),
                'prefix': 'sldu-',
                'ignore': '.*ZZZ',
               },
    'cd-113': {'key': 'census_geoid',
               'start': datetime.date(2012,1,1),
               'prefix': 'cd-',
               'ignore': None,
              },
}
