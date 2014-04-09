from fabric.api import env, task
from cheerwine.server import set_hosts, install_base, write_cron
from cheerwine.roles import Django, Postgres
from cheerwine.tasks import production

env.use_ssh_config = True

@task
def prepare_server():
    set_hosts('openstates')
    install_base(('libxslt-dev', 'libpq-dev'))

@task
def cron():
    write_cron('0 4 * * * /projects/openstates/virt/bin/python /projects/openstates/src/openstates/manage.py apireport  --settings=openstates.settings.production >> /projects/openstates/logs/apireport.log 2>&1\n' +
               '0 2 * * * /projects/openstates/virt/bin/python /projects/openstates/src/openstates/manage.py scout_push --settings=openstates.settings.production >> /projects/openstates/logs/scout_push.log 2>&1' , 'openstates')


openstates = Django(name='openstates',
                    ebs_size=10,
                    wsgi_module='openstates.wsgi:application',
                    repos={'openstates': 'git://github.com/sunlightlabs/openstates.org.git'},
                    files={'/projects/openstates/src/openstates/openstates/settings/production.py': 'settings.py',
                           '/projects/openstates/src/openstates/billy_local.py': 'billy_local.py',
                          },
                    nginx_locations={'/robots.txt': '/projects/openstates/src/openstates/',
                                     '/favicon.ico': '/projects/openstates/src/openstates/media/images/', },
                    uwsgi_extras={'processes': 12,
                                  'reload-on-rss': 200,
                                  'log-x-forwarded-for': 'true'
                                  # no-orphans
                                  # 'log-5xx': 'true',
                                  # 'log-slow': 700,
                                  # 'disable-logging': 'true',
                                 },
                    python3=False,
                    server_name='openstates.org',
                    dependencies=['-r openstates/requirements.txt'],
                    django_settings='openstates.settings.production'
                   )
