import os
import dj_database_url


if os.environ.get('DEBUG', 'true').lower() == 'false':
    DEBUG = False
    TEMPLATE_DEBUG = DEBUG
    ALLOWED_HOSTS = ['*']
    SECRET_KEY = os.environ['SECRET_KEY']
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = os.environ['EMAIL_HOST']
    EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
    EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
    EMAIL_PORT = '587'
    EMAIL_USE_TLS = True
else:
    DEBUG = True
    ALLOWED_HOSTS = ['*']
    SECRET_KEY = os.environ.get('SECRET_KEY', 'debug-secret-key')
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


DATABASE_URL = os.environ.get(
    'DATABASE_URL',
    'sqlite:///' + os.path.join(os.path.dirname(__file__), 'openstates.sqlite3')
)
DATABASES = {'default': dj_database_url.parse(DATABASE_URL)}
CONN_MAX_AGE = 60

if 'RAVEN_DSN' in os.environ:
    RAVEN_CONFIG = {
        'dsn': os.environ['RAVEN_DSN']
    }


# ADMINS = (
#     ('James Turk', 'james@openstates.org'),
# )
# MANAGERS = ADMINS

# stripe
STRIPE_PUBLIC_KEY = os.environ.get('STRIPE_PUBLIC_KEY', '')
STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY', '')
STRIPE_PLANS = [
    {
        'id': 'monthly5',
        'description': '$5/month',
    },
    {
        'id': 'monthly10',
        'description': '$10/month',
    },
    {
        'id': 'monthly20',
        'description': '$20/month',
    },
    {
        'id': 'monthly50',
        'description': '$50/month',
    },
    {
        'id': 'monthly100',
        'description': '$100/month',
    },
    {
        'id': 'yearly50',
        'description': '$50/year',
    },
    {
        'id': 'yearly100',
        'description': '$100/year',
    },
    {
        'id': 'yearly200',
        'description': '$200/year',
    },
    {
        'id': 'yearly500',
        'description': '$500/year',
    },
]


TIME_ZONE = 'UTC'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1

USE_I18N = True
USE_L10N = False
USE_TZ = True

MEDIA_ROOT = ''
MEDIA_URL = ''

DATE_FORMAT = 'Y-m-d'
TIME_FORMAT = 'H:i:s'
DATETIME_FORMAT = 'Y-m-d H:i:s'

STATIC_ROOT = os.path.join(os.path.dirname(__file__), '..', 'collected_static')
STATIC_URL = '/media/'
STATICFILES_DIRS = (
    os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'media')),
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates')),
        ],
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'donations.context_processors.stripe_settings',
            ],
            'loaders': [
                ('django.template.loaders.cached.Loader', (
                    'django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader',
                )),
            ]
        },
    },
]


MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'simplekeys.middleware.SimpleKeysMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

SIMPLEKEYS_ZONE_PATHS = [
    ('/api/v1/legislators/geo/', 'geo'),
    ('/api/v1/', 'default'),
]
SIMPLEKEYS_ERROR_NOTE = ('https://openstates.org/api/register/ for API key. '
                         'contact@openstates.org to raise limits')

ROOT_URLCONF = 'openstates.urls'

WSGI_APPLICATION = 'openstates.wsgi.application'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.humanize',
    'django.contrib.staticfiles',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.sites',
    'billy.web.api',
    'billy.web.admin',
    'billy.web.public',
    'markup_tags',
    'piston',
    'simplekeys',
    'raven.contrib.django.raven_compat',
)



DEFAULT_FROM_EMAIL = 'contact@openstates.org'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
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
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

LOGIN_REDIRECT_URL = '/'
