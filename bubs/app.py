import json
import pprint
import operator
from itertools import groupby

from flask import Flask, render_template, make_response, request
from flask import redirect, flash

import settings
from core import mongo


app = Flask(__name__, static_folder='static')
app.debug = settings.DEBUG
app.secret_key = settings.SECRET_KEY


@app.route("/report")
def report():
    meta = request.values.get('meta')
    abbr, chamber, term = meta.split(',')
    spec = dict(abbr=abbr, chamber=chamber, term=term)
    report = mongo.reports.find_one(spec)
    report['state'] = abbr

    party = operator.itemgetter('party')
    party_verbose = dict(r='Republican', d='Democratic')
    colormap = dict(r='#9A3E25', d='#156b90', o='#708259')
    points = []
    _points = list(sorted(report['points'], key=party))
    minx = 0
    maxx = 0
    for partyletter, iterator in groupby(_points, key=party):
        key = party_verbose.get(partyletter, 'Other')
        values = list(iterator)
        for val in values:
            size = val['size']
            if not size:
                size = 5
            val['size'] = size
        color = colormap[partyletter]
        points.append(dict(key=key, values=values, color=color))

        vals = [val['x'] for val in values]
        _minx = min(vals)
        _maxx = max(vals)
        minx = min(_minx, minx)
        maxx = max(_maxx, maxx)

    # Bubbles
    for series in points:
        for point in series['values']:
            url = 'http://static.openstates.org/photos/small/%s.jpg'
            url = url % point['legislator']['id']
            point['legislator']['photo_url'] = url
    report['points'] = json.dumps(points)

    report_meta = mongo.reports.find(fields=('abbr', 'chamber', 'term'))
    return render_template('report.html',
        report=report, report_meta=report_meta,
        minx=minx - 0.1, maxx=maxx + 0.1)


@app.route("/")
def home():
    report_meta = mongo.reports.find(fields=('abbr', 'chamber', 'term'))
    return render_template('home.html', report_meta=report_meta)


if __name__ == '__main__':
    app.run(debug=True)