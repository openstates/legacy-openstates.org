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
DATABASES = {'default': dj_database_url.config(default='postgis://opencivicdata:test@10.42.2.101/opencivicdata')}
ELASTICSEARCH_HOST = envvar('ELASTICSEARCH_HOST', 'http://localhost:9200')
TEMPLATE_DEBUG = DEBUG = envvar('DJANGO_DEBUG', 'False').lower() == 'true'
USE_LOCKSMITH = envvar('USE_LOCKSMITH', 'false').lower() == 'true'
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
    'opencivicdata.apps.BaseConfig',
    'imago',
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

# locksmith stuff
if USE_LOCKSMITH:
    INSTALLED_APPS += ('locksmith.auth.apps.LocksmithAuthConfig',)
    MIDDLEWARE_CLASSES += ('locksmith.auth.middleware.APIKeyMiddleware',)
    LOCKSMITH_REGISTRATION_URL = 'http://sunlightfoundation.com/api/accounts/register/#ocd'
    LOCKSMITH_HUB_URL = 'http://sunlightfoundation.com/api/analytics/'
    LOCKSMITH_API_NAME = 'opencivicdata'

BOUNDARIES_SHAPEFILES_DIR = 'shapefiles'
IMAGO_COUNTRY = 'us'
IMAGO_BOUNDARY_MAPPINGS = {
    'county-14': {'key': 'census_geoid',
                  'start': datetime.date(2015,1,1),
                  'prefix': 'county-',
                  'ignore': None,
                 },
    # 'county-13': {'key': 'census_geoid',
    #               'start': datetime.date(1980,1,1),
    #               'end': datetime.date(2015,1,1),
    #               'prefix': 'county-',
    #               'ignore': None,
    #              },

    'place-14': {'key': 'census_geoid',
                 'start': datetime.date(2015,1,1),
                 'prefix': 'place-',
                 'ignore': '.*CDP',
                },
    # 'place-13': {'key': 'census_geoid',
    #              'start': datetime.date(1980,1,1),
    #               'end': datetime.date(2015,1,1),
    #               'prefix': 'place-',
    #              'ignore': '.*CDP',
    #             },

    'sldl-14': {'key': 'census_geoid_14',
                'start': datetime.date(2015,1,1),
                'prefix': 'sldl-',
                'ignore': '.*ZZZ',
               },
    # 'sldl-13': {'key': 'census_geoid_12',
    #             'start': datetime.date(2012,1,1),
    #             'end': datetime.date(2015,1,1),
    #             'prefix': 'sldl-',
    #             'ignore': '.*ZZZ',
    #            },

    'sldu-14': {'key': 'census_geoid_14',
                'start': datetime.date(2015,1,1),
                'prefix': 'sldu-',
                'ignore': '.*ZZZ',
               },
    # 'sldu-13': {'key': 'census_geoid_12',
    #             'start': datetime.date(2012,1,1),
    #             'end': datetime.date(2015,1,1),
    #             'prefix': 'sldu-',
    #             'ignore': '.*ZZZ',
    #            },

    'cd-114': {'key': 'census_geoid',
               'start': datetime.date(2015,1,1),
               'prefix': 'cd-',
               'ignore': '.*ZZ',
              },
    # 'cd-113': {'key': 'census_geoid',
    #            'start': datetime.date(2012,1,1),
    #            'end': datetime.date(2015,1,1),
    #            'prefix': 'cd-',
    #            'ignore': '.*ZZ',
    #           },
}
