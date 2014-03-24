from fabric.api import env, task
from cheerwine.server import set_hosts, install_base
from cheerwine.roles import Django, Postgres

env.use_ssh_config = True

@task
def prepare_server():
    set_hosts('ocdapi')
    install_base(('unzip', 'gdal-bin'))

class API(Django):
    def __init__(self):
        super(API, self).__init__(
            name='ocdapi', ebs_size=10, wsgi_module='ocdapi.wsgi:application',
            repos={'ocdapi':'git://github.com/opencivicdata/api.opencivicdata.org.git',
                   'imago': 'git://github.com/opencivicdata/imago.git'},
            files={'/projects/ocdapi/src/ocdapi/ocdapi/settings/production.py':
                   'ocdapi/settings/production.py'},
            python3=True,
            dependencies=['-r ocdapi/requirements.txt'],
            django_settings='ocdapi.settings.production',
        )

    def syncdb(self):
        self.django('syncdb')
        self.django('migrate')
        #_dj('loadshapefiles -osldl-13,sldu-13,cd-113,place-13,county-13')
        #_dj('loaddivisions')

Postgres(15, 'api', 'api', postgis=True)
API()
