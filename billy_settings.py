import os

MONGO_HOST = os.environ.get('MONGO_HOST', 'localhost')
MONGO_PORT = os.environ.get('MONGO_PORT', 27017)
MONGO_DATABASE = os.environ.get('MONGO_DATABASE', 'fiftystates')
BOUNDARY_SERVICE_URL = os.environ.get('BOUNDARY_SERVICE_URL', 'http://localhost:9000/')
API_KEY = 'na'
API_BASE_URL = os.environ.get('API_BASE_URL', 'http://localhost:8000/api/v1/')

BILLY_PARTY_DETAILS = {
    # reminder: think through Singular, Plural, Adjective
    'Democratic': {'noun': 'Democrat', 'abbreviation': 'D'},
    'Republican': {'abbreviation': 'R'},
    'Independent': {'abbreviation': 'I'},
    'Democratic-Farmer-Labor': {'abbreviation': 'DFL',
                                'plural_noun': 'DFLers'},   # MN
    'Nonpartisan': {'abbreviation': 'NP', 'plural_noun': 'Nonpartisan'},  # NE
    'Unknown': {'abbreviation': '?', 'plural_noun': 'Unknown'},       # NY & PR
    'Partido Nuevo Progresista': {'abbreviation': 'PNP'},       # PR
    u'Partido Popular Democr\xe1tico': {'abbreviation': 'PPD'}, # PR
    'Carter County Republican': {'abbreviation': 'CCR'},    # TN
    'Working Families': {'abbreviation': 'WF'},             # NY & VT
    'Conservative': {'abbreviation': 'C'},                  # NY
    'Progressive': {'abbreviation': 'P'},                   # VT
    'Republican/Democratic': {'plural_noun': 'Republican/Democratic'},   # VT
}

BOUNDARY_SERVICE_SETS = 'sldl-14,sldu-14'

BILLY_ENABLE_DOCUMENT_VIEW = {
    'ak': True,
    'al': True,
    'ar': False,    # revisit
    'az': False,
    'ca': False,
    'co': False,    # revisit
    'ct': True,
    'dc': True,
    'de': True,
    'fl': True,
    'ga': False,
    'hi': True,
    'ia': True,
    'id': True,
    'il': True,
    'in': True,
    'ks': True,
    'ky': True,
    'la': False,    # revisit
    'ma': False,
    'md': True,
    'me': True,
    'mi': True,
    'mn': False,
    'mo': True,
    'ms': True,
    'mt': True,
    'nc': True,
    'nd': True,
    'ne': True,
    'nh': True,
    'nj': True,
    'nm': True,
    'nv': True,
    'ny': False,
    'oh': True,
    'ok': True,
    'or': True,
    'pa': False,    # revisit
    'pr': True,
    'ri': False,    # revisit
    'sc': True,
    'sd': False,
    'tn': True,
    'tx': False,    # revisit
    'ut': True,
    'va': False,
    'vt': True,
    'wa': False,    # revisit
    'wi': True,
    'wv': False,
    'wv': False
}
