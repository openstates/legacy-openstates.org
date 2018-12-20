from .utils import get_divisions_for


def test_anchorage_upper_redistricting():
    point = {'lat': 61.221, 'lon': -149.967}
    assert 'ocd-division/country:us/state:ak/sldu:k' in get_divisions_for(point)
    # assert 'ocd-division/country:us/state:ak/sldu:m' in get_divisions_for(point, SESSION_2013)

def test_juneau_upper_redistricting():
    point = {'lat': 58.222, 'lon': -134.876}
    assert 'ocd-division/country:us/state:ak/sldu:q' in get_divisions_for(point)
    # assert 'ocd-division/country:us/state:ak/sldu:c' in get_divisions_for(point, SESSION_2012)

def test_anchorage_lower_redistricting():
    point = {'lat': 61.207, 'lon': -149.814}
    assert 'ocd-division/country:us/state:ak/sldl:19' in get_divisions_for(point)
    # assert 'ocd-division/country:us/state:ak/sldl:22' in get_divisions_for(point, SESSION_2013)

def test_juneau_lower_redistricting():
    point = {'lat': 58.422, 'lon': -134.444}
    assert 'ocd-division/country:us/state:ak/sldl:34' in get_divisions_for(point)
    # assert 'ocd-division/country:us/state:ak/sldl:3' in get_divisions_for(point, SESSION_2012)
