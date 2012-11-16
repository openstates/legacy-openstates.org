import shapefile

def transform_file(filename, state, chamber, id_field, name_field):
    id_format = '{state}-{chamber}-{id}'

    shp = shapefile.Editor(filename)

    # find positions, ignore 'Delete' column
    for pos, field in enumerate(shp.fields[1:]):
        if field[0] == name_field:
            name_field_pos = pos
        if field[0] == id_field:
            id_field_pos = pos

    # open shp
    shp.field('P_STATE')
    shp.field('P_CHAMBER')
    shp.field('P_ID', size=200)
    shp.field('P_NAME', size=200)

    for record in shp.records:
        name = record[name_field_pos]
        old_id = record[id_field_pos]
        new_id = id_format.format(state=state, chamber=chamber, id=old_id)
        record.extend([state, chamber, record[name_field_pos], new_id, name])

    shp.save('newshapefiles/{state}-{chamber}'.format(state=state,
                                                      chamber=chamber))


transform_file('rawshapefiles/SB1_Reengrossed', 'la', 'upper', 'DISTRICT_I',
               'NAME')
