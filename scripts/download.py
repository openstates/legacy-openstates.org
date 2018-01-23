#!/usr/bin/env python

import os
import glob

import us

states = [s for s in us.STATES_AND_TERRITORIES if s not in us.OBSOLETE]
fips = sorted([s.fips for s in states])


def _download_file(URL, where):
    # create directory and work in it
    pop = os.path.abspath(os.getcwd())
    if not os.path.exists(where):
        os.makedirs(where)
    os.chdir(where)

    fname = os.path.basename(URL)
    if not os.path.exists(fname):
        os.system('wget %s' % (URL))

    os.chdir(pop)

def _list_files(*flags):
    files = os.listdir('.')
    for _file in files:
        for flag in flags:
            if _file.endswith(flag):
                yield _file


def _extract_cwd(path=None):
    pop = os.path.abspath(os.getcwd())
    if path:
        os.chdir(path)
    dirname = os.path.basename(os.getcwd())

    for f in glob.glob('*.zip'):
        os.system('unzip -o %s' % f)

    for path in _list_files("dbf", "prj", "shp", "xml", "shx"):
        os.renames(path, "../../shapefiles/{dirname}/{path}".format(**locals()))

    os.chdir(pop)

def _download_census_file(top, fips, what, year, where):

    if year == "13":
        URL = ("ftp://ftp2.census.gov/geo/tiger/{top}/{fips}/tl_rd{year}_{fips}_{what}.zip"
              ).format(**{"year": year, "what": what, "fips": fips, "top": top})
    else:
        URL = ("ftp://ftp2.census.gov/geo/tiger/{top}/{WHAT}/tl_{year}_{fips}_{what}.zip").format(
            **{ "year": year, "what": what, "WHAT": what.upper(), "fips": fips, "top": top, })

    _download_file(URL, where)

def download_state_leg_bounds():
    for fip in fips:
        _download_census_file("TIGER2014", fip, "sldl", "2014", "downloads/sldl-14")
        _download_census_file("TIGER2014", fip, "sldu", "2014", "downloads/sldu-14")

        _download_census_file("TIGERrd13_st", fip, "sldl", "13", "downloads/sldl-13")
        _download_census_file("TIGERrd13_st", fip, "sldu", "13", "downloads/sldu-13")
        
        _download_census_file("TIGER2012", fip, "sldl", "2012", "downloads/sldl-12")
        _download_census_file("TIGER2012", fip, "sldu", "2012", "downloads/sldu-12")

    for x in [
            "downloads/sldl-14", "downloads/sldu-14",
            "downloads/sldl-13", "downloads/sldu-13",
            "downloads/sldl-12", "downloads/sldu-12"
            ]:
        _extract_cwd(x)


def download_counties():
    _download_file("ftp://ftp2.census.gov/geo/tiger/TIGER2014/COUNTY/tl_2014_us_county.zip", "downloads/county-14")
    
    for fip in fips:
        _download_census_file("TIGERrd13_st", fip, "county10", "13", "downloads/county-13")
    
    for x in [
            "downloads/county-14",
            "downloads/county-13"
            ]:
        _extract_cwd(x)


def download_places():
    for fip in fips:
        _download_census_file("TIGER2014", fip, "place", "2014", "downloads/place-14")
        _download_census_file("TIGERrd13_st", fip, "place10", "13", "downloads/place-13")
    
    for x in [
            "downloads/place-14",
            "downloads/place-13"
            ]:
        _extract_cwd(x)


def download_nh_floterial():
    # New Hampshire has a second set of boundaries, that aren't served by the Census
    # Hosted here: https://www.nh.gov/oep/planning/services/gis/political-districts.htm
    _download_file("ftp://pubftp.nh.gov/OEP/NHHouseDists2012.zip", "downloads/nh-12")

    # Only want the floterial file, not the main district file
    pop = os.path.abspath(os.getcwd())
    os.chdir("downloads/nh-12")
    dirname = os.path.basename(os.getcwd())

    for f in glob.glob('*.zip'):
        os.system('unzip -o %s' % f)

    for path in _list_files("dbf", "prj", "shp", "xml", "shx"):
        if "NHHouse2012Float" in path:
            os.renames(path, "../../shapefiles/{dirname}/{path}".format(**locals()))

    os.chdir(pop)


def download_cds():
    _download_file("ftp://ftp2.census.gov/geo/tiger/TIGER2014/CD/tl_2014_us_cd114.zip", "downloads/cd-114")

    for fip in fips:
        _download_census_file("TIGERrd13_st", fip, "cd113", "13", "downloads/cd-113")
        _download_census_file("TIGERrd13_st", fip, "cd111", "13", "downloads/cd-111")
    
    for x in [
            "downloads/cd-114",
            "downloads/cd-113",
            "downloads/cd-111"
            ]:
        _extract_cwd(x)


def download_zcta():
    _download_file("ftp://ftp2.census.gov/geo/tiger/TIGER2014/ZCTA5/tl_2014_us_zcta510.zip", "downloads/zcta-14")
    _download_file("ftp://ftp2.census.gov/geo/tiger/TIGERrd13_st/nation/tl_rd13_us_zcta510.zip", "downloads/zcta-13")
    
    for x in [
            "downloads/zcta-14",
            "downloads/zcta-13"
            ]:
        _extract_cwd(x)


if __name__ == '__main__':
    download_nh_floterial()
    download_counties()
    download_places()
    download_cds()
    download_state_leg_bounds()
    # download_zcta()
