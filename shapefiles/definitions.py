"""
Configuration describing the shapefiles to be loaded.
"""
from django.contrib.gis.gdal.error import OGRIndexError
from datetime import date
import boundaries
import os
import us

states = [s for s in us.STATES_AND_TERRITORIES if s not in us.OBSOLETE]
state_fips = {s.fips: s.abbr.lower() for s in states}


def tiger_namer(feature):
    global OGRIndexError
    global state_fips

    try:
        fips_code = feature.get('STATEFP')
    except OGRIndexError:
        fips_code = feature.get('STATEFP10')

    try:
        name = feature.get('NAMELSAD')
    except OGRIndexError:
        name = feature.get('NAMELSAD10')

    try:
        geoid = feature.get('GEOID')
    except OGRIndexError:
        geoid = feature.get('GEOID10')

    state_abbrev = state_fips[fips_code].upper()
    name = name.encode('utf8').decode('latin-1')
    resp = u"{0} {1} {2}".format(state_abbrev, name, geoid)
    return resp


def geoid_tiger_namer(feature):
    try:
        geoid = feature.get('GEOID')
    except OGRIndexError:
        geoid = feature.get('GEOID10')
    return geoid


def nh_12_namer(feature):
    '''
    New Hampshire's floterial district shapefiles have only one field:
    an abbreviated district name ("AA#" format). This has to be
    crosswalked to useful information.

    The crosswalk is roughly based on this Census file:
    www2.census.gov/geo/docs/maps-data/data/NH_2012_Floterials.txt
    '''

    abbr = feature.get('NHHouse201')
    # There are two shapefiles that don't correspond to any floterial
    # These need unique IDs, which end with 'zzz' so that they'll be ignored
    if not abbr:
        import datetime
        unique_key = datetime.datetime.now()
        return "{}zzz".format(unique_key)

    path = os.path.join(
        os.path.abspath(os.getcwd()),
        'shapefiles',
        'nh_12_crosswalk.csv'
    )

    with open(path, 'r') as f:
        # Due to a bug in `boundaries`, need to `import csv` here
        import csv
        reader = list(csv.DictReader(f))
        (row, ) = [x for x in reader if x['NHHouse201'] == abbr]

        STATE_ABBREV = 'NH'
        name = row['NAMELSAD']
        geoid = row['GEOID']

    resp = "{0} {1} {2}".format(STATE_ABBREV, name, geoid)
    return resp


def geoid_nh_12_namer(feature):
    abbr = feature.get('NHHouse201')
    if not abbr:
        import datetime
        unique_key = datetime.datetime.now()
        return "{}zzz".format(unique_key)

    path = os.path.join(
        os.path.abspath(os.getcwd()),
        'shapefiles',
        'nh_12_crosswalk.csv'
    )

    with open(path, 'r') as f:
        # Due to a bug in `boundaries`, need to `import csv` here
        import csv
        reader = list(csv.DictReader(f))
        (row, ) = [x for x in reader if x['NHHouse201'] == abbr]

        geoid = row['GEOID']

    return geoid


class index_namer(object):
    def __init__(self, prefix):
        self.prefix = prefix
        self.count = 0

    def __call__(self, feature):
        self.count += 1
        return '{0}{1}'.format(self.prefix, self.count)


CENSUS_URL = 'http://www.census.gov/geo/maps-data/data/tiger.html'
LAST_UPDATE = date(2015, 4, 24)
defaults = dict(last_updated=LAST_UPDATE,
                domain='United States',
                authority='US Census Bureau',
                source_url=CENSUS_URL,
                license_URL=CENSUS_URL,
                data_url=CENSUS_URL,
                notes='',
                extra='{}',
               )


# congressional districts
boundaries.register('cd-114',
                    singular='cd-114',
                    file='cd-114/',
                    name_func=tiger_namer,
                    id_func=geoid_tiger_namer,
                    **defaults
                   )

boundaries.register('cd-113',
                    singular='cd-113',
                    file='cd-113/',
                    name_func=tiger_namer,
                    id_func=geoid_tiger_namer,
                    **defaults
                   )

boundaries.register('cd-111',
                    singular='cd-111',
                    file='cd-111/',
                    name_func=tiger_namer,
                    id_func=geoid_tiger_namer,
                    **defaults
                   )

# Zip Code Tabulation Areas
boundaries.register('zcta-14',
                    singular='zcta-14',
                    file='zcta-14/',
                    name_func=boundaries.attr('ZCTA5CE10'),
                    id_func=geoid_tiger_namer,
                    start_date=date(2015, 1, 1),
                    **defaults
                   )

boundaries.register('zcta-13',
                    singular='zcta-13',
                    file='zcta-13/',
                    name_func=boundaries.attr('ZCTA5CE10'),
                    id_func=geoid_tiger_namer,
                    start_date=date(2012, 1, 1),
                    end_date=date(2015, 1, 1),
                    **defaults
                   )

boundaries.register('sldl-14',
                    singular='sldl-14',
                    file='sldl-14/',
                    name_func=tiger_namer,
                    id_func=geoid_tiger_namer,
                    start_date=date(2015, 1, 1),
                    **defaults
                   )

boundaries.register('sldl-13',
                    singular='sldl-13',
                    file='sldl-13/',
                    name_func=tiger_namer,
                    id_func=geoid_tiger_namer,
                    start_date=date(2012, 1, 1),
                    end_date=date(2015, 1, 1),
                    **defaults
                   )

boundaries.register('sldu-14',
                    singular='sldu-14',
                    file='sldu-14/',
                    name_func=tiger_namer,
                    id_func=geoid_tiger_namer,
                    start_date=date(2015, 1, 1),
                    **defaults
                   )

boundaries.register('sldu-13',
                    singular='sldu-13',
                    file='sldu-13/',
                    name_func=tiger_namer,
                    id_func=geoid_tiger_namer,
                    start_date=date(2012, 1, 1),
                    end_date=date(2015, 1, 1),
                    **defaults
                   )

boundaries.register('county-14',
                    singular='county-14',
                    file='county-14/',
                    encoding='latin-1',
                    name_func=tiger_namer,
                    id_func=geoid_tiger_namer,
                    start_date=date(2015, 1, 1),
                    **defaults
                   )

boundaries.register('county-13',
                    singular='county-13',
                    file='county-13/',
                    encoding='latin-1',
                    name_func=tiger_namer,
                    id_func=geoid_tiger_namer,
                    start_date=date(2012, 1, 1),
                    end_date=date(2015, 1, 1),
                    **defaults
                   )

boundaries.register('place-14',
                    singular='place-14',
                    file='place-14/',
                    name_func=tiger_namer,
                    id_func=geoid_tiger_namer,
                    start_date=date(2015, 1, 1),
                    encoding='latin-1',
                    **defaults
                   )

boundaries.register('place-13',
                    singular='place-13',
                    file='place-13/',
                    name_func=tiger_namer,
                    id_func=geoid_tiger_namer,
                    start_date=date(2012, 1, 1),
                    end_date=date(2015, 1, 1),
                    encoding='latin-1',
                    **defaults
                   )

boundaries.register('nh-12',
                    singular='nh-12',
                    file='nh-12/',
                    name_func=nh_12_namer,
                    id_func=geoid_nh_12_namer,
                    start_date=date(2013, 1, 1),
                    last_updated=LAST_UPDATE,
                    domain='United States',
                    authority='NH Office of Energy and Planning',
                    source_url='http://www.nh.gov/oep/planning/services/gis/political-districts.htm',
                    license_URL='http://www.nh.gov/oep/planning/services/gis/political-districts.htm',
                    data_url='ftp://pubftp.nh.gov/OEP/NHHouseDists2012.zip',
                    notes='',
                    extra='{}',
                   )
