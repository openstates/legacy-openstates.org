import os
import sys
import json
import itertools
import shapefile
from shapely.geometry import Polygon
from shapely.geos import PredicateError

state_fips = {
    '01': 'al', '02': 'ak', '04': 'az', '05': 'ar', '06': 'ca', '08': 'co',
    '09': 'ct', '10': 'de', '11': 'dc', '12': 'fl', '13': 'ga', '15': 'hi',
    '16': 'id', '17': 'il', '18': 'in', '19': 'ia', '20': 'ks', '21': 'ky',
    '22': 'la', '23': 'me', '24': 'md', '25': 'ma', '26': 'mi', '27': 'mn',
    '28': 'ms', '29': 'mo', '30': 'mt', '31': 'ne', '32': 'nv', '33': 'nh',
    '34': 'nj', '35': 'nm', '36': 'ny', '37': 'nc', '38': 'nd', '39': 'oh',
    '40': 'ok', '41': 'or', '42': 'pa', '44': 'ri', '45': 'sc', '46': 'sd',
    '47': 'tn', '48': 'tx', '49': 'ut', '50': 'vt', '51': 'va', '53': 'wa',
    '54': 'wv', '55': 'wi', '56': 'wy', '72': 'pr'
}


def generate_mss(mss_id, shpfile, selector=None):
    shp = shapefile.Reader(shpfile)

    # find the position of the selector in fields
    candidate_selectors = (selector,) if selector else ('SLDLST', 'SLDUST')
    for fpos, f in enumerate(shp.fields):
        if f[0] in candidate_selectors:
            # the selector pos is 1 less than the pos in fields
            selector = f[0]
            spos = fpos - 1

    # create dict of selectors to polygons
    shapes = {}
    for rec, shape in zip(shp.records(), shp.shapes()):
        if rec[spos] == 'ZZZ':
            continue
        if shape.shapeType in (shapefile.POLYGON, shapefile.POLYGONZ):
            shapes[rec[spos]] = Polygon(shape.points)
        else:
            raise Exception("Unknown Shape Type: %s" % shape.shapeType)

    # color choices
    colors = ('@c1', '@c2', '@c3', '@c4', '@c5', '@c6', '@c7', '@c8', '@c9')
    colors = itertools.cycle(colors)

    # pick a color
    shape_colors = {}
    for name1, shape1 in shapes.iteritems():
        disallowed_colors = set([None])
        # find overlapping colors
        for name2, shape2 in shapes.iteritems():
            try:
                if name1 != name2 and shape1.intersects(shape2):
                    disallowed_colors.add(shape_colors.get(name2))
            except PredicateError:
                # not sure why these happen, but we'll count them as collisions
                disallowed_colors.add(shape_colors.get(name2))
        # pick a color that matches
        proposed_color = None
        if len(disallowed_colors) == 9:
            proposed_color = '@grey'
            print 'had to use grey for ', name1
        else:
            while proposed_color in disallowed_colors:
                proposed_color = colors.next()
        shape_colors[name1] = proposed_color

    # write the .mss
    mss = """{0} {{ line-color: #999; line-width: 0.5; polygon-opacity: 0.5; }}
@c1: #f3b05d;
@c2: #e1582c;
@c3: #932700;
@c4: #b3bf7e;
@c5: #7f985e;
@c6: #5e6f3e;
@c7: #8cbcb5;
@c8: #698784;
@c9: #204e50;
\n\n
""".format(mss_id)
    return mss + '\n'.join(
        '{0}[{1}="{2}"] {{ polygon-fill: {3}; }}'.format(mss_id, selector,
                                                         id, color)
        for id, color in shape_colors.iteritems())


def generate_mml(shpfile, state=None, chamber=None, selector=None):
    shp = shapefile.Reader(shpfile)
    bbox = list(shp.bbox)
    if bbox[0] > 180:
        bbox = [-180, -85, 180, 85]

    # figure out chamber from fields
    if not chamber:
        if shp.fields[2][0] == 'SLDLST':
            chamber = 'lower'
        elif shp.fields[2][0] == 'SLDUST':
            chamber = 'upper'

    # figure out state from FIPS code in a record
    if not state and shp.fields[1][0] == 'STATEFP':
        state = state_fips[shp.record(0)[0]]

    projname = state + chamber

    mml = {'format': 'png', 'metatile': 2, 'minzoom': 4, 'maxzoom': 12,
           'description': '', 'attribution': '', 'legend': '',
           'Stylesheet': ["style.mss"],
           'name': projname, 'bounds': bbox,
           'srs': "+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0.0 +k=1.0 +units=m +nadgrids=@null +wktext +no_defs +over"}
    mml['center'] = [(bbox[0] + bbox[2])/2, (bbox[1] + bbox[3])/2, 6]
    mml['Layer'] = [{'geometry': 'polygon', 'id': 'districts', 'class': '',
                     'Datasource': {'file': '../../'+shpfile}, 'extent': bbox,
                    'srs-name': 'autodetect', 'srs': '', 'advanced': {},
                     'name': 'districts'}]

    mml['interactivity'] = {'layer': 'districts',
                            'template_teaser': '{{NAMELSAD}}'}

    # make dir
    os.makedirs(os.path.join('project', projname))
    # write mml
    json.dump(mml, open(os.path.join('project', projname, 'project.mml'), 'w'), indent=2)
    # write mss
    mss = generate_mss('#districts', shpfile, selector)
    open(os.path.join('project', projname, 'style.mss'), 'w').write(mss)


import sys
arg = sys.argv[1]
generate_mml('shapefiles/sldl/PVS_12_v2_sldl_%s.shp' % arg)
generate_mml('shapefiles/sldu/PVS_12_v2_sldu_%s.shp' % arg)
