                    wsgi_module='openstates.wsgi:application',
                    nginx_locations={'/robots.txt': '/projects/openstates/src/openstates/',
                                     '/favicon.ico': '/projects/openstates/src/openstates/media/images/', },
                    uwsgi_extras={'processes': 12,
                                  'reload-on-rss': 200,
                                  'log-x-forwarded-for': 'true'
                                 },
