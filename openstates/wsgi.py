import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "openstates.settings")

try:
    import newrelic.agent
    newrelic.agent.initialize('/home/openstates/newrelic.ini')
except Exception as e:
    print("newrelic couldn't be initialized:", e)

# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.
from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
