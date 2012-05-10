"""
Configuration describing the shapefiles to be loaded.
"""
from datetime import date
import boundaries

def tiger_namer(feature):
    state_fips = {
        '01': 'al', '02': 'ak', '04': 'az', '05': 'ar', '06': 'ca', '08': 'co',
        '09': 'ct', '10': 'de', '11': 'dc', '12': 'fl', '13': 'ga', '15': 'hi',
        '16': 'id', '17': 'il', '18': 'in', '19': 'ia', '20': 'ks', '21': 'ky',
        '22': 'la', '23': 'me', '24': 'md', '25': 'ma', '26': 'mi', '27': 'mn',
        '28': 'ms', '29': 'mo', '30': 'mt', '31': 'ne', '32': 'nv', '33': 'nh',
        '34': 'nj', '35': 'nm', '36': 'ny', '37': 'nc', '38': 'nd', '39': 'oh',
        '40': 'ok', '41': 'or', '42': 'pa', '44': 'ri', '45': 'sc', '46': 'sd',
        '47': 'tn', '48': 'tx', '49': 'ut', '50': 'vt', '51': 'va', '53': 'wa',
        '54': 'wv', '55': 'wi', '56': 'wy', '72': 'pr',
    }

    # VA exception
    if 'VAPOTHER' in feature.feature.fields:
        return "VA %s" % feature.get('DISTRICT_N')

    fips_code = feature.get('STATEFP10')
    state_abbrev = state_fips[fips_code].upper()

    return "%s %s" % (state_abbrev, feature.get('NAMELSAD10'))

class index_namer(object):
    def __init__(self, prefix):
        self.prefix = prefix
        self.i = 0

    def __call__(self, feature):
        out = '{0}{1}'.format(self.prefix, self.i)
        self.i += 1
        return out


SHAPEFILES = {
    #'SLDL': {
    #    'file': 'sldl',
    #    'singular': 'SLDL',
    #    'kind_first': True,
    #    'ider': utils.index_namer('sldl-'),
    #    'namer': tiger_namer,
    #    'authority': 'US Census Bureau',
    #    'domain': 'United States',
    #    'last_updated': date(2010, 12, 12),
    #    'href': 'http://www.census.gov/geo/www/tiger/tgrshp2010/tgrshp2010.html',
    #    'notes': '',
    #    'encoding': '',
    #},

    #'SLDU': {
    #    'file': 'sldu',
    #    'singular': 'SLDU',
    #    'kind_first': True,
    #    'ider': utils.index_namer('sldu-'),
    #    'namer': tiger_namer,
    #    'authority': 'US Census Bureau',
    #    'domain': 'United States',
    #    'last_updated': date(2010, 12, 12),
    #    'href': 'http://www.census.gov/geo/www/tiger/tgrshp2010/tgrshp2010.html',
    #    'notes': '',
    #    'encoding': '',
    #},

    #'CD': {
    #    'file': 'cd.shp',
    #    'singular': 'CD',
    #    'kind_first': True,
    #    'ider': utils.index_namer('cd-'),
    #    'namer': tiger_namer,
    #    'authority': 'US Census Bureau',
    #    'domain': 'United States',
    #    'last_updated': date(2010, 12, 12),
    #    'href': 'http://www.census.gov/geo/www/tiger/tgrshp2010/tgrshp2010.html',
    #    'notes': '',
    #    'encoding': '',
    #},

    #'ZCTA': {
    #    'file': 'zcta.shp',
    #    'singular': 'ZCTA',
    #    'kind_first': True,
    #    'ider': utils.simple_namer(['ZCTA5CE10']),
    #    'namer': utils.simple_namer(['ZCTA5CE10']),
    #    'authority': 'US Census Bureau',
    #    'domain': 'United States',
    #    'last_updated': date(2010, 1, 1),
    #    'href': 'http://www.census.gov/geo/www/tiger/tgrshp2010/tgrshp2010.html',
    #    'notes': '',
    #    'encoding': '',
    #},
}


boundaries.register('Congressional Districts',
                    singular='Congressional District',
                    domain='United States',
                    file='cd/',
                    last_updated=date(2010, 12, 12),
                    name_func=tiger_namer,
                    id_func=index_namer('cd-'),
                    authority='US Census Bureau',
                    source_url='http://www.census.gov/geo/www/tiger/tgrshp2010/tgrshp2010.html',
                    licence_url='http://www.census.gov/geo/www/tiger/tgrshp2010/tgrshp2010.html',
                    data_url='http://www.census.gov/geo/www/tiger/tgrshp2010/tgrshp2010.html',
                    notes='',
                   )
