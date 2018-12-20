geo.openstates.org
---

This repo is a Django project for deployment of the Open States geospatial lookup, taking geographic coordinates and returning district information. It contains the REST API from the [`represent-boundaries`](https://github.com/rhymeswithcycle/represent-boundaries) project to actually power the lookup.

## Running locally

### Requirements

- `wget`
- Python 3
- `pip install -r requirements.txt`
- GDAL 1.11
- Postgres

### Running

#### Database

- Set up your Postgres database, accessible at the URI specified in `ocdapi/settings.py`, including creating a login user with the given username and password
- Enable PostGIS for the database
- Run migrations for this Django project, using `python manage.py migrate`. If you hit a GDAL error at the start, check that you're on the proper version of GDAL, and that your Django is fixed for [this GDAL versioning issue](https://stackoverflow.com/questions/18643998/geodjango-geosexception-error).
- Import the OCD IDs, using `python manage.py loaddivisions us`

#### Boundaries

- Download the shapefiles using `python scripts/download.py`
- Register these boundaries to the database by running `python manage.py loadshapefiles`. Depending on how many sets of shapefiles you're loading, this could take a long time.
- Process the relationships between OCD divisions and these boundaries, using `python manage.py loadmappings`
  - Due to Django versioning issues, this may fail due to Imago not creating tables properly with `python manage.py migrate`. If so, create the Imago tables manually in `psql`.

#### API

Run the server using `python manage.py runserver`.

## Testing

_Currently non-functional, since the deprecation of Imago; should be updated_

- `pip install -r requirements-test.txt`
- `pytest`
