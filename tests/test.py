from datetime import date

from opencivicdata.api.client import VagrantOCDAPI


api = VagrantOCDAPI()

# SESSION_2013 = date(2013, 6, 1)
# SESSION_2015 = date(2015, 6, 1)

def get_divisions_for(place, date=date.today()):
    # DATE_FORMAT = '%Y-%m-%d'
    # place['date'] = date.strftime(DATE_FORMAT)
    return [x['id'] for x in api.divisions(**place)]


def test_sunlight_in_dc_ward_2():
    SUNLIGHT_HQ = {'lat': 38.907148, 'lon': -77.043064}
    assert 'ocd-division/country:us/district:dc/ward:2' in get_divisions_for(SUNLIGHT_HQ)

def test_ak_zcta_99801_redistricting():
    ''' https://sunlightfoundation.supportbee.com/tickets/4308139 '''

    ZCTA_CENTER = {'lat': 57.65, 'lon': -134.00}
    assert 'ocd-division/country:us/state:ak/sldl:34' in get_divisions_for(ZCTA_CENTER)
    assert 'ocd-division/country:us/state:ak/sldl:35' in get_divisions_for(ZCTA_CENTER)

    # assert 'ocd-division/country:us/state:ak/sldl:31' in get_divisions_for(ZCTA_CENTER, SESSION_2013)
    # assert 'ocd-division/country:us/state:ak/sldl:32' in get_divisions_for(ZCTA_CENTER, SESSION_2013)

def test_pa_zip_plus_four_19147_5823_redistricting():
    ''' https://sunlightfoundation.supportbee.com/tickets/4377604 '''

    ZP4_CENTER = {'lat': 39.931011, 'lon': -75.153176}
    assert 'ocd-division/country:us/state:pa/sldl:184' in get_divisions_for(ZP4_CENTER)

    # assert 'ocd-division/country:us/state:pa/sldl:185' in get_divisions_for(ZP4_CENTER, SESSION_2013)

def test_mi_ann_arbor_redistricting():
    NORTHERN_ANN_ARBOR = {'lat': 42.2994, 'lon': -83.7568}
    assert 'ocd-division/country:us/state:mi/sldl:55' in get_divisions_for(NORTHERN_ANN_ARBOR)

    # assert 'ocd-division/country:us/state:mi/sldl:153' in get_divisions_for(NORTHERN_ANN_ARBOR, SESSION_2013)

def test_az_east_redistricting():
    EASTERN_AZ = {'lat': 34, 'lon': -109.5}
    assert 'ocd-division/country:us/state:az/sldl:7' in get_divisions_for(EASTERN_AZ)

    # assert 'ocd-division/country:us/state:mi/sldl:5' in get_divisions_for(EASTERN_AZ, SESSION_2013)

def test_ne_scottsbluff():
    SCOTTSBLUFF = {'lat': 41.8672, 'lon': -103.6608}
    assert 'ocd-division/country:us/state:ne/sldu:48' in get_divisions_for(SCOTTSBLUFF)

    # assert get_divisions_for(SCOTTSBLUFF, SESSION_2013) == get_divisions_for(SCOTTSBLUFF)
