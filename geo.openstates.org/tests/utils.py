from opencivicdata.api.client import VagrantOCDAPI

api = VagrantOCDAPI()

def get_divisions_for(place):
    """
    Get the OCD IDs for a given lat/lon

    place should be a dict containing two keys -- `lat' and `lon'.
    """
    return [x['id'] for x in api.divisions(**place)]
