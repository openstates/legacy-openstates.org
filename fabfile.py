from fabric.api import env, task
from cheerwine.server import set_hosts, install_base
from cheerwine.roles import Django, Postgres
from cheerwine.config import config

env.use_ssh_config = True

@task
def prepare_server():
    set_hosts('openstates')
    install_base(('libxslt-dev', 'libpq-dev'))

openstates = Django(name='openstates', ebs_size=10, wsgi_module='openstates.wsgi:application',
                    repos={'openstates': 'git://github.com/sunlightlabs/openstates.org.git'},
                    files={'/projects/openstates/src/openstates/openstates/settings/production.py': 'production.py',
                           '/projects/openstates/src/openstates/billy_local.py': 'billy_local.py'
                          },
                    nginx_locations={'/robots.txt': '/projects/openstates/src/openstates/',
                                     '/favicon.ico': '/projects/openstates/src/openstates/media/images/',
                              },
                    uwsgi_extras={'processes': 12,
                                  'reload-on-rss': 200,
                                  'log-x-forwarded-for': 'true'
                                  # no-orphans
                                  # 'log-5xx': 'true',
                                  # 'log-slow': 700,
                                  # 'disable-logging': 'true',
                                 },
                    python3=False,
                    dependencies=['-r openstates/requirements.txt'],
                    django_settings='openstates.settings.production'
                   )
