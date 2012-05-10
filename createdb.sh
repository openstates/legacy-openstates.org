createuser pentagon -P
createdb pentagon
psql -d pentagon -f /usr/share/postgresql/9.1/contrib/postgis-1.5/postgis.sql
psql -d pentagon -f /usr/share/postgresql/9.1/contrib/postgis-1.5/spatial_ref_sys.sql 
