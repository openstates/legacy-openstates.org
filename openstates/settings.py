import os


if os.environ.get('DEBUG', 'true').lower() == 'false':
    DEBUG = False
    TEMPLATE_DEBUG = DEBUG
    ALLOWED_HOSTS = ['*']
    SECRET_KEY = os.environ['SECRET_KEY']
else:
    DEBUG = True
    ALLOWED_HOSTS = ['*']
    SECRET_KEY = os.environ.get('SECRET_KEY', 'debug-secret-key')


ADMINS = (
    ('James Turk', 'james.p.turk@gmail.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(os.path.dirname(__file__), 'openstates.sqlite3'),
    }
}

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


TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    'donations.context_processors.stripe_settings',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'openstates.urls'

WSGI_APPLICATION = 'openstates.wsgi.application'

TEMPLATE_DIRS = (
    os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates')),
)

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
)

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
