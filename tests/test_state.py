from .utils import get_divisions_for


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

def test_pittsburgh_redistricting():
    ''' https://sunlightfoundation.supportbee.com/tickets/3956255 '''
    
    ADDRESS = {'lat': 40.495, 'lon': -80.053}
    assert 'ocd-division/country:us/state:pa/sldl:20' in get_divisions_for(ADDRESS)
    assert 'ocd-division/country:us/state:pa/sldl:42' in get_divisions_for(ADDRESS)

    # assert 'ocd-division/country:us/state:pa/sldl:16' get_divisions_for(ADDRESS, SESSION_2013)
    # assert 'ocd-division/country:us/state:pa/sldl:42' get_divisions_for(ADDRESS, SESSION_2013)
