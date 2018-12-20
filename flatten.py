import requests
import os
import pymongo
from django.template.defaultfilters import slugify

SERVER = 'http://localhost:9999'
BASE = 'html/'

db = pymongo.MongoClient()['fiftystates']


def flatten(url):
    filename = os.path.join(BASE, url.lstrip('/'), 'index.html')
    if os.path.exists(filename):
        print('skipping', filename)
        return
    resp = requests.get(SERVER + url)
    if resp.status_code != 200:
        print('broken', url)
        return
    try:
        os.makedirs(os.path.dirname(filename))
    except OSError:
        pass
    with open(filename, 'wb') as out:
        out.write(resp.content)


def flatten_basics():
    flatten('/')
    flatten('/reportcard/')
    # for mdata in db.metadata.find():
    #     state = mdata['_id']
    #     flatten(f'/{state}/')
    #     flatten(f'/{state}/legislators/')
    #     flatten(f'/{state}/committees/')
    #     flatten(f'/{state}/bills/')

def flatten_legislators():
    for leg in db.legislators.find():
        state = leg['state']
        slug = slugify(leg['full_name'])
        flatten(f'/{state}/legislators/{leg["leg_id"]}/{slug}/')
        flatten(f'/{state}/legislators/{leg["leg_id"]}/')
        # flatten(f'/{state}/legislators/{leg["leg_id"]}/votes')

def flatten_bills():
    for b in db.bills.find():
        session = b['session']
        bill_id = b['bill_id']
        state = b['state']
        flatten(f'/{state}/bills/{session}/{bill_id}/')


def flatten_votes():
    for v in db.votes.find():
        state = v['state']
        flatten(f'/{state}/votes/{v["_id"]}/')


# flatten_basics()
# flatten_legislators()
# flatten_bills()
flatten_votes()
