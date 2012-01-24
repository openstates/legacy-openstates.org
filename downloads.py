import os
import glob
import shutil


def download_census_shapefiles(slug, url, download=True):
    dirname = 'downloads/{0}/'.format(slug)
    if download:
        os.makedirs(dirname)
    os.chdir(dirname)
    if download:
        os.system('wget ' + url)

    # unzip
    for f in glob.glob('*.zip'):
        os.system('unzip -o %s' % f)

    os.chdir('../..')


process_census_shapefiles('sldu',
  'ftp://ftp2.census.gov/geo/tiger/TIGER2010/SLDU/2010/*.zip')
process_census_shapefiles('sldl',
  'ftp://ftp2.census.gov/geo/tiger/TIGER2010/SLDL/2010/*.zip')
#process_census_shapefiles('cd',
#  'ftp://ftp2.census.gov/geo/tiger/TIGER2010/CD/111/tl_2010_us_cd111.zip')
#process_census_shapefiles('zcta',
#  'ftp://ftp2.census.gov/geo/tiger/TIGER2010/ZCTA5/2010/tl_2010_us_zcta510.zip')
