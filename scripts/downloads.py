import os
import glob
import shutil


def download_census_shapefiles(slug, url, download=True):
    dirname = 'shapefiles/{0}/'.format(slug)
    if download:
        if not os.path.exists(dirname):
            os.makedirs(dirname)

    os.chdir(dirname)
    if download:
        if not os.path.exists(os.path.basename(url)):
            os.system('wget ' + url)

    # unzip
    for f in glob.glob('*.zip'):
        os.system('unzip -o %s' % f)

    os.chdir('../..')


fips = ('01', '02', '04', '05', '06', '08', '09', '10', '11', '12', '13', '15',
        '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27',
        '28', '29', '30', '31' ,'32', '33', '34', '35', '36', '37', '38', '39',
        '40', '41', '42', '44', '45', '46', '47', '48', '49', '50', '51', '53',
        '54', '55', '56', '60', '66', '69', '72', '78')


def download_census_file(fips, what):
    # create directory and work in it
    if not os.path.exists('downloads'):
        os.mkdir('downloads')
    os.chdir('downloads')

    URL = ("ftp://ftp2.census.gov/geo/tiger/"
           "TIGERrd{year}_st/{fips}/tl_rd{year}_{fips}_{what}.zip").format(**{
               "year": "13",
               "what": what,
               "fips": fips
           })

    fname = os.path.basename(URL)
    if not os.path.exists(fname):
        os.system('wget %s' % (URL))

    os.chdir('..')



def download_state_legislative_districts():
    for fip in fips:
        download_census_file(fip, 'sldl')
        download_census_file(fip, 'sldu')


def download_counties():
    for fip in fips:
        download_census_file(fip, 'county10')
#        download_census_file(fip, 'cousub10')


def download_congressional_districts():
    for fip in fips:
        download_census_file(fip, 'cd113')


def list_files(_type, *flags):
    files = os.listdir('.')
    for _file in files:
        for flag in flags:
            if _file.endswith(flag) and _type in _file:
                yield _file


def save_shapefiles(*args, **kwargs):
    args = list(args)

    os.chdir('downloads')

    for f in glob.glob('*.zip'):
        os.system('unzip -o %s' % f)

    special_cases = kwargs

    for x in kwargs:
        args.append(x)

    for type in args:
        # create type dir

        name = type
        if name in special_cases:
            name = special_cases[name]

        dir = '../shapefiles/{0}'.format(name)
        if not os.path.exists(dir):
            os.mkdir(dir)

        # copy files over
        lis = " ".join(list_files(type, "shp", "shx", "prj", "xml", "dbf"))
        if lis.strip() == "":
            raise Exception

        os.system('mv %s ../shapefiles/%s' % (lis, name))

        # do 2d conversion
        for f in glob.glob(dir + '/*.shp'):
            os.system('ogr2ogr -f "ESRI Shapefile" -overwrite {0} '
                      '{1} -nlt POLYGON'.format(dir, f))

        os.system('cp ../shapefiles/exceptions/{0}/* '
                  '../shapefiles/{0}/'.format(name))


    os.chdir('..')


download_census_shapefiles('zcta',
    'http://www2.census.gov/geo/tiger/TIGER2012/ZCTA5/tl_2012_us_zcta510.zip')

download_state_legislative_districts()
download_counties()
download_congressional_districts()

save_shapefiles('sldl', 'sldu',
                county10='county',
#                cousub10='cousub',
                cd113='cd')
