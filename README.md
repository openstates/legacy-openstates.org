Issues?
-------

Issues with the opencivicdata.org API should be filed at the [api.opencivicdata.org issue tracker](https://sunlight.atlassian.net/browse/OCD/component/10001)

All Open Civic Data issues can be browsed and filed at [the Open Civic Data JIRA instance](https://sunlight.atlassian.net/browse/OCD/).

What is this?
-------------

This repo is essentially just a Django project for deployment- actual API code is a part of several other projects:

* [boundaries](https://github.com/rhymeswithcycle/represent-boundaries) - backs GIS portion
* [imago](https://github.com/opencivicdata/imago) - people, bills, events, etc.


To get started:

    python scripts/downloads.py                 # downloads shapefiles
    # create a postgres database & user and add to a local_settings.py file
    ./manage.py syncdb
    ./manage.py migrate
    ./manage.py loadshapefiles
    ./manage.py loaddivisions https://raw.github.com/opencivicdata/ocd-division-ids/master/identifiers/country-us.csv
    ./manage.py loadgeomapping county-13 1980-01-01 https://raw.github.com/opencivicdata/ocd-division-ids/master/mappings/us-census-geoids.csv
    ./manage.py loadgeomapping place-13 1980-01-01 https://raw.github.com/opencivicdata/ocd-division-ids/master/mappings/us-census-geoids.csv
    # also need to load mappings for zctas, cds, sldus, sldls
