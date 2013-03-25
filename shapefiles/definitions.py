"""
Configuration describing the shapefiles to be loaded.
"""
from datetime import date
import boundaries


state_fips = {
    '01': 'al', '02': 'ak', '04': 'az', '05': 'ar', '06': 'ca', '08': 'co',
    '09': 'ct', '10': 'de', '11': 'dc', '12': 'fl', '13': 'ga', '15': 'hi',
    '16': 'id', '17': 'il', '18': 'in', '19': 'ia', '20': 'ks', '21': 'ky',
    '22': 'la', '23': 'me', '24': 'md', '25': 'ma', '26': 'mi', '27': 'mn',
    '28': 'ms', '29': 'mo', '30': 'mt', '31': 'ne', '32': 'nv', '33': 'nh',
    '34': 'nj', '35': 'nm', '36': 'ny', '37': 'nc', '38': 'nd', '39': 'oh',
    '40': 'ok', '41': 'or', '42': 'pa', '44': 'ri', '45': 'sc', '46': 'sd',
    '47': 'tn', '48': 'tx', '49': 'ut', '50': 'vt', '51': 'va', '53': 'wa',
    '54': 'wv', '55': 'wi', '56': 'wy', '60': 'as', '66': 'gu', '69': 'mp',
    '72': 'pr', '78': 'vi'
}


def tiger_namer(feature):
    global state_fips
    fips_code = feature.get("STATEFP")
    state_abbrev = state_fips[fips_code].upper()
    return "%s %s" % (state_abbrev, feature.get('NAME'))


def tiger10_namer(feature):
    global state_fips
    fips_code = feature.get("STATEFP10")
    state_abbrev = state_fips[fips_code].upper()
    return "%s %s" % (state_abbrev, feature.get('NAMELSAD10'))



class index_namer(object):
    def __init__(self, prefix):
        self.prefix = prefix
        self.count = 0

    def __call__(self, feature):
        self.count += 1
        return '{0}{1}'.format(self.prefix, self.count)

CENSUS_URL = 'https://www.census.gov/rdo/data/113th_congressional_and_new_state_legislative_district_plans.html'

# congressional districts
boundaries.register('cd',
                    singular='cd',
                    domain='United States',
                    file='cd/',
                    last_updated=date(2012, 11, 15),
                    name_func=tiger_namer,
                    id_func=index_namer('cd-'),
                    authority='US Census Bureau',
                    source_url=CENSUS_URL,
                    licence_url=CENSUS_URL,
                    data_url=CENSUS_URL,
                    notes='',
                   )

# Zip Code Tabulation Areas
boundaries.register('zcta',
                    singular='zcta',
                    domain='United States',
                    file='zcta/',
                    last_updated=date(2012, 11, 15),
                    name_func=boundaries.attr('ZCTA5CE10'),
                    id_func=index_namer('zcta-'),
                    authority='US Census Bureau',
                    source_url=CENSUS_URL,
                    licence_url=CENSUS_URL,
                    data_url=CENSUS_URL,
                    notes='',
                   )


boundaries.register('sldl',
                    singular='sldl',
                    domain='United States',
                    file='sldl/',
                    last_updated=date(2012, 11, 15),
                    name_func=tiger_namer,
                    id_func=index_namer('sldl-'),
                    authority='US Census Bureau',
                    source_url=CENSUS_URL,
                    licence_url=CENSUS_URL,
                    data_url=CENSUS_URL,
                    notes='',
                   )

boundaries.register('sldu',
                    singular='sldu',
                    domain='United States',
                    file='sldu/',
                    last_updated=date(2012, 11, 15),
                    name_func=tiger_namer,
                    id_func=index_namer('sldu-'),
                    authority='US Census Bureau',
                    source_url=CENSUS_URL,
                    licence_url=CENSUS_URL,
                    data_url=CENSUS_URL,
                    notes='',
                   )

boundaries.register('county',
                    singular='county',
                    domain='United States',
                    file='county/',
                    last_updated=date(2012, 11, 15),
                    name_func=tiger10_namer,
                    id_func=index_namer('county-'),
                    authority='US Census Bureau',
                    source_url=CENSUS_URL,
                    licence_url=CENSUS_URL,
                    data_url=CENSUS_URL,
                    notes='',
                   )
