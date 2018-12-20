import os
import datetime
import dj_database_url
from django.core.exceptions import ImproperlyConfigured

def envvar(name, default=None):
    result = os.environ.get(name, default)
    if result is None:
        raise ImproperlyConfigured('missing required environment variable ' + name)
    return result

# env variables
SECRET_KEY = envvar('SECRET_KEY', 'ITSASECRET')
RAVEN_DSN = envvar('RAVEN_DSN', '')
ALLOWED_HOSTS = envvar('ALLOWED_HOSTS', '*').split(',')
DATABASES = {'default': dj_database_url.config(default='postgis://openstates:test@localhost/openstates', conn_max_age=600)}
ELASTICSEARCH_HOST = envvar('ELASTICSEARCH_HOST', 'http://localhost:9200')
TEMPLATE_DEBUG = DEBUG = envvar('DJANGO_DEBUG', 'False').lower() == 'true'

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
TEST_RUNNER = 'django.test.runner.DiscoverRunner'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.contenttypes',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'boundaries',
    'imago',
    'opencivicdata.apps.BaseConfig',
    'pupa',
)
if RAVEN_DSN:
    INSTALLED_APPS += ('raven.contrib.django.raven_compat',)
    RAVEN_CONFIG = {'dsn': RAVEN_DSN}


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
        'default':{
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

BOUNDARIES_SHAPEFILES_DIR = 'shapefiles'
IMAGO_COUNTRY = 'us'
IMAGO_BOUNDARY_MAPPINGS = {
    'sldl-17': {'key': 'census_geoid_14',
                'prefix': 'sldl-',
                'ignore': '.*ZZZ',
               },
    'sldl-16': {'key': 'census_geoid_14',
                'prefix': 'sldl-',
                'ignore': '.*ZZZ',
               },
    'sldl-15': {'key': 'census_geoid_14',
                'prefix': 'sldl-',
                'ignore': '.*ZZZ',
               },
    'sldl-14': {'key': 'census_geoid_14',
                'prefix': 'sldl-',
                'ignore': '.*ZZZ',
               },
    'sldl-13': {'key': 'census_geoid_14',
                'prefix': 'sldl-',
                'ignore': '.*ZZZ',
               },

    'sldu-17': {'key': 'census_geoid_14',
                'prefix': 'sldu-',
                'ignore': '.*ZZZ',
               },
    'sldu-16': {'key': 'census_geoid_14',
                'prefix': 'sldu-',
                'ignore': '.*ZZZ',
               },
    'sldu-15': {'key': 'census_geoid_14',
                'prefix': 'sldu-',
                'ignore': '.*ZZZ',
               },
    'sldu-14': {'key': 'census_geoid_14',
                'prefix': 'sldu-',
                'ignore': '.*ZZZ',
               },
    'sldu-13': {'key': 'census_geoid_14',
                'prefix': 'sldu-',
                'ignore': '.*ZZZ',
               },

    'nh-12': {'key': 'census_geoid_14',
              'prefix': 'sldl-',
              'ignore': '.*zzz'
             },
}
