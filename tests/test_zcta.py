from .utils import get_divisions_for


def test_ak_zcta_99801_redistricting():
    ''' https://sunlightfoundation.supportbee.com/tickets/4308139 '''

    ZCTA_CENTER = {'lat': 57.65, 'lon': -134.00}
    assert 'ocd-division/country:us/state:ak/sldl:35' in get_divisions_for(ZCTA_CENTER)

    # assert 'ocd-division/country:us/state:ak/sldl:31' in get_divisions_for(ZCTA_CENTER, SESSION_2013)
    # assert 'ocd-division/country:us/state:ak/sldl:32' in get_divisions_for(ZCTA_CENTER, SESSION_2013)

def test_pa_zip_plus_four_19147_5823_redistricting():
    ''' https://sunlightfoundation.supportbee.com/tickets/4377604 '''

    ZP4_CENTER = {'lat': 39.931011, 'lon': -75.153176}
    assert 'ocd-division/country:us/state:pa/sldl:184' in get_divisions_for(ZP4_CENTER)

    # assert 'ocd-division/country:us/state:pa/sldl:185' in get_divisions_for(ZP4_CENTER, SESSION_2013)
