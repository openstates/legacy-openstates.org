Actual API code is a part of several other projects:

* [boundaries](https://github.com/rhymeswithcycle/represent-boundaries) - backs GIS portion
* [locust](https://github.com/opencivicdata/locust) - ocd-division portion
* [imago](https://github.com/opencivicdata/imago) - people, bills, events, etc.


To get started w/ boundaries and locust:

    python scripts/downloads.py                 # downloads shapefiles
    # create a postgres database & user and add to a local_settings.py file
    ./manage.py syncdb
    ./manage.py migrate
    ./manage.py loadshapefiles
    ./manage.py loaddivisions https://raw.github.com/opencivicdata/ocd-division-ids/master/identifiers/country-us.csv
    ./manage.py loadgeomapping county-13 1980-01-01 https://raw.github.com/opencivicdata/ocd-division-ids/master/mappings/us-census-geoids.csv
