from opencivicdata.api.client import VagrantOCDAPI

api = VagrantOCDAPI()

SUNLIGHT_HQ = {"lat": 38.907148, "lon": -77.043064}

def get_divisions_for(place):
    return [x['id'] for x in api.divisions(**place)]


def test_sunlight_ward():
    """
    Test that Sunlight HQ is in DC Ward 2
    """
    divisions = get_divisions_for(SUNLIGHT_HQ)
    assert 'ocd-division/country:us/district:dc/ward:2' in divisions
