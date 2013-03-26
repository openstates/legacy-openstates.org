#!/usr/bin/env python

import urllib2
import json
import sys


URL_BASE = "http://localhost:8000"



def query_bs(lat, lon):
    path = "/boundaries/?contains={lat},{lon}".format(**locals())
    URL = "%s%s" % (URL_BASE, path)
    return json.load(urllib2.urlopen(URL))


def entries(fp):
    with open(fp, 'r') as fd:
        for line in fd:
            lat, lon, blocks = line.split(",", 2)
            yield {"lat": lat, "lon": lon,
                   "blocks": [x.strip() for x in blocks.split(",")]}

for entry in entries(sys.argv[1]):
    obj = query_bs(entry['lat'], entry['lon'])
    response = map(lambda x: x['external_id'], obj['objects'])
    for e in entry['blocks']:
        try:
            assert e in response
        except AssertionError:
            print e, response
            raise
    print "[ ok ] - %s / %s" % (entry['lat'], entry['lon'])
