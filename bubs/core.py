import time
import pickle
import logging
import functools
import urllib2
import socket

import pymongo
from sunlight import openstates

import settings


conn = pymongo.MongoClient(host=settings.MONGO_HOST)
mongo = getattr(conn, settings.MONGO_DATABASE_NAME)
if settings.MONGO_PASSWORD:
    mongo.authenticate(settings.MONGO_USER, settings.MONGO_PASSWORD)


logging.basicConfig(level=logging.DEBUG)

# Bypass Tim's...improvements...to the varnish config.
import sunlight.services.openstates.service
service_url = 'http://localhost:8000/api/v1'


class CachedAttr(object):
    '''Computes attr value and caches it in the instance.'''

    def __init__(self, method, name=None):
        self.method = method
        self.name = name or method.__name__

    def __get__(self, inst, cls):
        if inst is None:
            return self
        result = self.method(inst)
        setattr(inst, self.name, result)
        return result


# def memoize_methodcalls(func, dumps=pickle.dumps):
#     '''Cache the results of the function for each input it gets called with.
#     '''
#     cache = func.cache = {}
#     @functools.wraps(func)
#     def memoizer(self, *args, **kwargs):
#         key = dumps((args, kwargs))
#         if args not in cache:
#             cache[args] = func(self, *args, **kwargs)
#         return cache[args]
#     return memoizer


class TooFewBillsError(Exception):
    '''Raised when the search window doesn't contain enough
    bills for a meaningful calculation, where enough is
    arbitrarily defined as 1000.
    '''


class IterBills(object):

    PER_PAGE = 500

    @CachedAttr
    def data(self):
        return {}

    @CachedAttr
    def bill_metadata(self):
        spec = {
            'state': self.abbr,
            'chamber': self.chamber,
            'per_page': self.PER_PAGE}
        if self.term and not self.session:
            if isinstance(self.term, basestring):
                # Search the specified term.
                spec['search_window'] = 'term:' + self.term
            else:
                # Search the current term.
                spec['search_window'] = 'term'
        elif self.session:
            if isinstance(self.session, basestring):
                # Search the specified session.
                spec['search_window'] = 'session:' + self.session
            else:
                # Search the current session.
                spec['search_window'] = 'session'

        logging.info('Fetching bill metadata...')
        page = 1
        meta = []
        while True:
            spec.update(page=page)
            logging.debug('Fetching metadata: %r' % spec)
            more_meta = openstates.bills(**spec)
            if not more_meta:
                break
            meta += more_meta
            if self.limit and self.limit < (page * self.PER_PAGE):
                break
            page += 1
        logging.info('...done.')

        if self.limit:
            meta = meta[:self.limit]

        if len(meta) < 300:
            # If the term or session contains too few bills for a
            # meaningful calculation, complain/bail.
            msg = 'Too few bills found (%d); aborting. %r'
            data = dict(
                abbr=self.abbr,
                session=self.session,
                term=self.term)
            raise TooFewBillsError(msg % (len(meta), data,))

        return meta

    def __init__(self, abbr, chamber, session=None, term=None, limit=None):
        if not any([term, session]):
            raise ValueError('Supply either a term or session.')
        self.abbr = abbr
        self.session = session
        self.term = term
        self.chamber = chamber
        self.limit = limit
        self.per_page = min(limit or self.PER_PAGE, self.PER_PAGE)

    def __iter__(self):
        self.index = 0
        data = self.data
        while True:
            try:
                yield next(self)
                self.index += 1
            except IndexError:
                return

    def next(self):
        data = self.data
        bill = self.bill_metadata[self.index]
        bill_id = bill['id']
        if bill_id in data:
            return data[bill_id]
        else:
            logging.debug('Fetching bill: %r' % bill_id)
            for x in range(3):
                try:
                    bill = openstates.bill(bill_id)
                    break
                except socket.timeout:
                    logging.info('Got a timeout; sleeping 2 seconds.')
                    time.sleep(2)
                except urllib2.URLError:
                    logging.info('Got a bad url; sleeping 2 seconds.')
                    continue
            else:
                raise Exception('Fail whale')
            data[bill_id] = bill
            return bill

    def itervotes(self):
        for bill in self:
            for vote in bill['votes']:
                if vote['chamber'] == bill['chamber']:
                    yield vote


class IterLegislators(object):
    '''A caching iterator over legislator data.
    '''
    def __init__(self, abbr, chamber):
        self.abbr = abbr
        self.chamber = chamber
        self._data = None
        self._detail_data = {}

    def __iter__(self):
        return iter(self.metadata)

    @CachedAttr
    def metadata(self):
        logging.debug('Fetching legislators')
        return openstates.legislators(
            state=self.abbr, chamber=self.chamber, active=False)

    def detail(self, leg_id):
        self.metadata
        logging.debug('Fetching legislator %r' % id)
        return openstates.legislator_detail(leg_id)


class DictSetDefault(object):
    '''Context manager like getattr, but yields a default value,
    and sets on the instance on exit:

    with DictSetDefault(somedict, key, []) as attr:
        attr.append('something')
    print obj['something']
    '''
    def __init__(self, obj, key, default_val):
        self.obj = obj
        self.key = key
        self.default_val = default_val

    def __enter__(self):
        val = self.obj.get(self.key, self.default_val)
        self.val = val
        return val

    def __exit__(self, exc_type, exc_value, traceback):
        self.obj[self.key] = self.val
