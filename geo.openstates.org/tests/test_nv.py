from .utils import get_divisions_for


def test_las_vegas_upper_redistricting():
    point = {'lat': 36.1539, 'lon': -115.2014}
    assert 'ocd-division/country:us/state:nv/sldu:3' in get_divisions_for(point)
    # assert 'ocd-division/country:us/state:nv/sldu:11' in get_divisions_for(point, SESSION_2013)

def test_reno_upper_redistricting():
    point = {'lat': 39.5570, 'lon': -119.8134}
    assert 'ocd-division/country:us/state:nv/sldu:13' in get_divisions_for(point)
    # assert 'ocd-division/country:us/state:nv/sldu:14' in get_divisions_for(point, SESSION_2013)

def test_las_vegas_lower_redistricting():
    point = {'lat': 36.1826, 'lon': -115.1300}
    assert 'ocd-division/country:us/state:nv/sldl:11' in get_divisions_for(point)
    # assert 'ocd-division/country:us/state:nv/sldl:6' in get_divisions_for(point, SESSION_2013)

def test_reno_lower_redistricting():
    point = {'lat': 39.4960, 'lon': -119.7904}
    assert 'ocd-division/country:us/state:nv/sldl:24' in get_divisions_for(point)
    # assert 'ocd-division/country:us/state:nv/sldl:27' in get_divisions_for(point, SESSION_2013)
