import sys
import json
import logging
import socket
from itertools import product, combinations
from collections import Counter, defaultdict
from operator import itemgetter

import rpy2
import networkx
import numpy as np
from pandas import DataFrame
from sunlight import response_cache, openstates
from pscl import Rollcall

from core import (
    mongo, IterBills, IterLegislators,
    TooFewBillsError, DictSetDefault)


response_cache.enable('mongo')
response_cache.logger.setLevel(10)


class DataQualityError(Exception):
    '''Raised if calculation is aborted due to data quality issues.
    '''


class ScoreCalculator(object):
    '''Given a state, chamber, and term or session, calculate
    the cosponsorship pagerank, effectiveness, and ideal point
    scores for each legislator.
    '''
    def __init__(self, abbr, chamber, meta, term=None, session=None):
        self.meta = meta
        self.abbr = abbr
        self.session = session
        self.term = term
        self.chamber = chamber
        self.bills = IterBills(
            abbr, chamber, session=session, term=term)
        self.legislators = IterLegislators(abbr, chamber)
        self.leg_deets = {}

    def get_pagerank(self):
        '''Create a co-sponsorship digraph based on the information from
        the Open States API and calculate the pagerank of each legislator.
        '''
        ids = set()
        G = networkx.DiGraph()
        number_of_bills = 0

        for bill in self.bills:
            sponsors = bill['sponsors']
            # if len(sponsors) < 2:
            #     continue

            # Separate sponsors into primary, secondary.
            primary = []
            secondary = []
            for sponsor in sponsors:
                if sponsor['leg_id'] is None:
                    continue
                if sponsor['type'] == 'primary':
                    primary.append(sponsor['leg_id'])
                else:
                    secondary.append(sponsor['leg_id'])
                ids.add(sponsor['leg_id'])

            # Add them to the network.
            if primary and secondary:
                for primary, secondary in product(primary, secondary):
                    try:
                        G[secondary][primary]['weight'] += 1
                    except KeyError:
                        G.add_edge(secondary, primary, weight=1)
            elif primary:
                for edge in combinations(primary, r=2):
                    for p1, p2 in [edge, edge[::-1]]:
                        try:
                            G[p1][p2]['weight'] += 1
                        except KeyError:
                            G.add_edge(p1, p2, weight=1)

        if not G.nodes():
            # Known offenders: CO, AR, CT, ID, and others.
            # Reuturn all zeroes.
            # return dict.fromkeys(ids, 0)
            data = dict(abbr=self.abbr, chamber=self.chamber)
            msg = ("Can't generate PageRank scores due to lack of secondary "
                   "sponsorship data: %r.")
            raise DataQualityError(msg % (data,))

        return networkx.pagerank_numpy(G)

    def get_effectiveness(self):
        '''Create an effectiveness score for each legislator relative to
        all the others based on the extent to which bills by each leg'r
        are passed on the chamber of origin, the other chamber, or into law.
        '''
        # Multipliers used below.
        multipliers = dict(
            passed_own=1,
            passed_other=2,
            signed=20)

        legislators = defaultdict(Counter)
        number_of_bills = 0
        chamber = self.chamber

        # Calculate the scores.
        for bill in self.bills:
            sponsors = bill['sponsors']

            # Separate sponsors into primary, secondary.
            primary = []
            secondary = []
            for sponsor in sponsors:
                if sponsor['type'] == 'primary':
                    primary.append(sponsor['leg_id'])
                else:
                    secondary.append(sponsor['leg_id'])

            for sponsor in primary:
                if chamber == 'upper':
                    other_chamber = 'lower'
                else:
                    other_chamber = 'upper'
                if bill['action_dates']['passed_%s' % self.chamber]:
                    legislators[sponsor]['passed_own'] += 1
                if bill['action_dates']['passed_%s' % other_chamber]:
                    legislators[sponsor]['passed_other'] += 1
                if bill['action_dates']['signed']:
                    legislators[sponsor]['signed'] += 1

        # Compute the scores.
        vals = []
        detail = self.legislators.detail
        for leg_id, counter in legislators.items():
            if leg_id is None:
                continue
            with DictSetDefault(self.leg_deets, leg_id, detail(leg_id)) as deets:
                for key, multiplier in multipliers.items():
                    score = counter[key] * multiplier
                vals.append(score)
                deets['eff_stats'] = dict(counter, score=score)

        if not vals:
            raise DataQualityError('No effectiveness data available.')

        scoresdict = {}
        for key in multipliers:
            scoresdict[key] = [d[key] for d in legislators.values()]

        percentiles = defaultdict(dict)
        for key, scores in scoresdict.items():
            for n in range(1, 101):
                percentiles[key][n] = np.percentile(scores, n)

        # Normalize the scores.
        vals = np.array(map(float, vals))
        normed = (vals / sum(vals) * 250)
        normed = dict(zip(vals, normed))
        newvals = {}
        for leg_id in legislators:
            if leg_id is None:
                continue
            leg_deets = self.leg_deets[leg_id]
            with DictSetDefault(leg_deets, 'eff_stats', {}) as eff_stats:
                for key, percentiledict in percentiles.items():
                    score = eff_stats.get(key, 0)
                    eff_stats[key] = score
                    percentile = 0
                    if set(percentiledict.values()) == set([0.0]):
                        percentile = 0
                    else:
                        for n, val in percentiledict.items():
                            if score < val:
                                break
                            else:
                                percentile = n
                    eff_stats[key + '_percentile'] = percentile
                newvals[leg_id] = normed.get(eff_stats.get('score', 0))
        return newvals

    def get_idealpoints(self):
        '''Get ideal point for each legislator.
        '''
        YES = float(1)
        NO = float(2)
        OTHER = float(3)

        votedata = defaultdict(dict)
        vote_vals = dict(yes_votes=YES, no_votes=NO, other_votes=OTHER)
        leg_ids = set()
        chamber_ids = [leg['id'] for leg in self.legislators.metadata]

        vote_keys = 'yes_votes, no_votes, other_votes'.split(', ')
        for vote in self.bills.itervotes():
            for k in vote_keys:
                for voter in vote[k]:
                    leg_id = voter['leg_id']
                    if leg_id is None:
                        continue
                    if leg_id not in chamber_ids:
                        continue
                    leg_ids.add(leg_id)
                    votedata[vote['id']][leg_id] = vote_vals[k]

        # Convert the dict into a pandas DataFrame.
        dataframe = DataFrame(votedata, index=leg_ids)
        dataframe.fillna(value=9)

        # Create a rollcall object similar to pscl's.
        rollcall = Rollcall.from_dataframe(dataframe,
            yea=[YES],
            nay=[NO],
            missing=[OTHER],
            not_in_legis=0.0,
            legis_names=tuple(leg_ids))

        # Here they are.
        xbar = rollcall.ideal().xbar

        # Now guess the polarity.
        polarities = defaultdict(list)
        parties = {}
        polarity_parties = defaultdict(Counter)
        for legislator in self.legislators:
            leg_id = legislator['leg_id']
            if leg_id not in xbar:
                continue
            parties[leg_id] = legislator.get('party', 'o')
            sign = 0 < xbar[leg_id]
            polarities[sign].append(leg_id)

        for polarity, leg_ids in polarities.items():
            for leg_id in leg_ids:
                party = parties[leg_id]
                letter = party.lower()[0]
                if letter not in 'rd':
                    letter = 'o'
                polarity_parties[polarity][letter] += 1

        # If a the parties are clustered on distinct sides use that,
        # else on the side where most are clustered, assign that
        # side to the most frequently occuring party.
        polarity_results = {}
        for polarity, partydict in polarity_parties.items():
            most_frequent = max(partydict, key=partydict.get)
            polarity_results[polarity] = most_frequent

        # If the polarity appears to be backwards, reverse it.
        if polarity_results[True] != 'r':
            xbar = {leg_id: -n for (leg_id, n) in xbar.items()}

        return xbar

    def get_scores(self):
        '''Helper function for ScoreCalculator monster.
        '''
        logging.info('Starting %r' % ([self.abbr, self.chamber, self.term],))

        logging.info('Starting pagerank calculation...')
        pageranks = self.get_pagerank()
        logging.info('...done')

        logging.info('Starting effectiveness calculation...')
        effectiveness = self.get_effectiveness()
        logging.info('...done')

        logging.info('Starting ideal point calculation...')
        idealpoints = self.get_idealpoints()
        logging.info('...done')

        return dict(
            effectiveness=effectiveness,
            pageranks=pageranks,
            idealpoints=idealpoints)

    def import_scores(self, meta):
        '''Write the scores into mongo.
        '''
        keep_keys = (
            'first_name', 'last_name', 'party', 'eff_stats',
            'photo_url', 'district', 'full_name', 'id')

        def party_letter(party):
            parties = 'rd'
            letter = party.lower()[0]
            if letter in parties:
                return letter
            else:
                return 'o'

        scores = self.get_scores()

        # Get a set of all ids.
        ids = set(scores['idealpoints'].keys())
        ids = filter(None, ids)

        points = []
        leg_deets = self.leg_deets
        for leg_id in ids:
            legislator = self.leg_deets.get(leg_id)
            if legislator is None:
                legislator = self.legislators.detail(leg_id)
            party = party_letter(legislator.get('party', 'o'))
            logging.debug('Party is %r' % party)

            leg_keys = (
                'first_name', 'last_name', 'district',
                'photo_url', 'full_name', 'id', 'eff_stats')
            for key in tuple(legislator):
                if key not in leg_keys:
                    legislator.pop(key)

            # Calculate the point data.
            point = dict(
                x=scores['idealpoints'][leg_id],
                # If no effectiveness score, s/he got no bills passed.
                y=scores['effectiveness'].get(leg_id, 0),
                # If no PR score, s/he had no consponsorships.
                size=scores['pageranks'].get(leg_id, 0),
                party=party,
                legislator=legislator,
                )
            points.append(point)

        report = dict(
            name=self.meta['name'],
            term=self.term,
            term_name='%s Term' % self.term,
            chamber_name=self.meta['chambers'][self.chamber]['name'],
            abbr=self.abbr,
            chamber=self.chamber,
            points=points)
        mongo.reports.save(report)
        return report


def import_all(*abbrs):
    for state in openstates.all_metadata():
        if abbrs and state['abbreviation'] not in abbrs:
            continue
        abbr = state['abbreviation']
        if abbr in ('co', 'ar', 'ct', 'al', 'dc', 'id'):
            continue
        meta = openstates.state_metadata(abbr)
        for chamber in meta['chambers']:
            latest_term = sorted(meta['terms'], key=itemgetter('start_year'))
            term = latest_term.pop()
            spec = dict(
                term=term['name'],
                abbr=abbr,
                chamber=chamber)
            if mongo.reports.find_one(spec):
                logging.debug('Skipping %r' % spec)
                continue
            try:
                calc = ScoreCalculator(abbr, chamber, meta, term=term['name'])
                report = calc.import_scores(meta)
            except DataQualityError as exc:
                logging.exception(exc)
                logging.error('No party data: skipping %r' % ([abbr, chamber, term],))
            except TooFewBillsError as exc:
                logging.exception(exc)
                logging.error('Too few bills found: skipping %r' % ([abbr, chamber, term],))
            except rpy2.rinterface.RRuntimeError as exc:
                logging.exception(exc)
                logging.error('R error: skipping %r' % ([abbr, chamber, term],))


if __name__ == '__main__':
    # import_scores(*sys.argv[1:])
    # import_scores('ny', 'lower', term='2011-2012')
    logging.basicConfig(level=logging.DEBUG)
    socket.setdefaulttimeout(5)
    mongo.reports.drop()
    import_all()
