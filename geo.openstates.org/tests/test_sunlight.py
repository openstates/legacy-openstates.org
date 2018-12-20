from .utils import get_divisions_for


def test_sunlight_in_dc_ward_2():
    SUNLIGHT_HQ = {'lat': 38.907148, 'lon': -77.043064}
    assert 'ocd-division/country:us/district:dc/ward:2' in get_divisions_for(SUNLIGHT_HQ)
