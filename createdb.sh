createdb pentagon
createlang plpgsql pentagon
psql -d pentagon -f /usr/share/postgresql/8.4/contrib/postgis-1.5/postgis.sql
psql -d pentagon -f /usr/share/postgresql/8.4/contrib/postgis-1.5/spatial_ref_sys.sql 
