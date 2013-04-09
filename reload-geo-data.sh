#!/bin/bash

DEPLOYMENT="dev"
SET_YEAR_ID="13"

function manage {
    if [ "x$1" = "x" ]; then
        echo "Need a command to run."
        exit 1
    fi
    python manage.py $@ --settings settings.${DEPLOYMENT}
}

manage sqlclear locust | manage dbshell
manage syncdb

STATES=$(python -c "import us; print '\n'.join([x.abbr for x in us.STATES])")


for state in $STATES; do
    state=$(echo $state | tr '[A-Z]' '[a-z]')
    echo $state
    manage loaddivisions "https://raw.github.com/opencivicdata/ocd-division-ids/master/identifiers/country-us/state-${state}-census.csv"
    manage loadgeomapping ${SET_YEAR_ID} "https://raw.github.com/opencivicdata/ocd-division-ids/master/mappings/country-us/state-${state}-id_to_censusgeo.csv"
done
