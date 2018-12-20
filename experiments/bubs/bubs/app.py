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
    return _report(template_name='report.html')


@app.route("/report_slblog")
def report_slblog():
    return _report(template_name='report_sunlight.html')


@app.route("/report_mainetoday")
def report_maintoday():
    return _report(template_name='report_mainetoday.html')


def _report(template_name):
    meta = request.values.get('meta')
    abbr, chamber, term = meta.split(',')
    abbr = abbr.lower()
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
    avg_size = sum(pt['size'] for pt in _points)/len(_points)
    for partyletter, iterator in groupby(_points, key=party):
        key = party_verbose.get(partyletter, 'Other')
        values = list(iterator)
        for val in values:
            size = val['size']
            if not size:
                size = avg_size
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

    fields = ('abbr', 'chamber', 'term')
    report_meta = list(mongo.reports.find(projection=fields))
    report_meta.sort(key=operator.itemgetter('abbr'))
    for rpt in report_meta:
        rpt.pop('_id')
        rpt['abbr'] = rpt['abbr'].upper()
    selected = dict(zip(fields, (abbr, chamber, term)))
    return render_template(template_name,
        report=report, report_meta=report_meta,
        minx=minx - 0.1, maxx=maxx + 0.1, selected=selected)


@app.route("/")
def home():
    report_meta = mongo.reports.find(fields=('abbr', 'chamber', 'term'))
    return render_template('home.html', report_meta=report_meta)


@app.route("/_wget_index/")
def wget_index():
    '''An index view for wget -m purposes.
    '''
    fields = ('abbr', 'chamber', 'term')
    report_meta = list(mongo.reports.find(fields=fields))
    return render_template('wget_index.html', report_meta=report_meta)



if __name__ == '__main__':
    app.run(debug=True)
