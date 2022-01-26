import census_debug as cd
import geopandas as gpd
import json
import os


def read_london_ward_geojson():

    # Get London GeoJSON
    london_jsonfile = "data/json_files/London_Ward_Boundaries.json"
    if not os.path.exists(london_jsonfile):

        # Census Ward Boundaries as GeoJSON
        census_jsonfile = "data/json_files/Census_Merged_Wards_(December_2011)_Boundaries.json"
        if not os.path.exists(census_jsonfile):

            # Get Census Boundaries as GeoPandas
            shapefile = 'data/Census_Merged_Wards_(December_2011)_Boundaries/Census_Merged_Wards_(December_2011)_Boundaries.shp'
            cd.start_timer()
            gdf = gpd.read_file(shapefile)
            cd.print_timer('Read ward shapefile')      # 2s 122MB
            # Convert coordinates
            gdf.to_crs(epsg=4326, inplace=True)
            # Write GeoJSON
            cd.start_timer()
            gdf.to_file(
                "data/json_files/Census_Merged_Wards_(December_2011)_Boundaries.json", driver='GeoJSON')
            cd.print_timer('Write ward GeoJson')       # 46s 336MB

        with open(census_jsonfile) as f:
            cd.start_timer()
            census_wards = json.load(f)
            cd.print_timer('Read ward GeoJson')        # 15s 336MB

        london_wards = census_wards
        london_wards['features'] = list(filter(
            lambda f: f['properties']['lad11cd'].startswith('E090000'), london_wards['features']))
        with open(london_jsonfile, 'w') as f:
            cd.start_timer()
            json.dump(london_wards, f)
            cd.print_timer('Write london ward GeoJson')    # 14s 6MB
    else:
        with open(london_jsonfile) as f:
            cd.start_timer()
            london_wards = json.load(f)
            cd.print_timer('Read london ward GeoJson')     # 0.14s 6MB
    return london_wards


def read_london_lad_geojson():

    # Get LAD GeoJSON
    london_jsonfile = "data/json_files/London_LAD_Boundaries.json"
    if not os.path.exists(london_jsonfile):

        lad_jsonfile = "data/json_files/Local_Authority_Districts_(December_2011)_Boundaries_EW_BFC.json"
        if not os.path.exists(lad_jsonfile):

            # Get Census LAD Boundaries as GeoPandas
            shapefile = 'data/Local_Authority_Districts_(December_2011)_Boundaries_EW_BFC/Local_Authority_Districts_(December_2011)_Boundaries_EW_BFC.shp'
            cd.start_timer()
            ladgdf = gpd.read_file(shapefile)
            cd.print_timer('Read lad shapefile')        # 0.46s 38MB
            # Convert coordinates
            ladgdf.to_crs(epsg=4326, inplace=True)
            # Write GeoJSON
            cd.start_timer()
            ladgdf.to_file(lad_jsonfile, driver='GeoJSON')
            cd.print_timer('Write lad GeoJson')        # 12s 103MB

        with open(lad_jsonfile) as f:
            cd.start_timer()
            census_lads = json.load(f)
            cd.print_timer('Read lad GeoJson')         # 2.7s 103MB

        london_lads = census_lads
        london_lads['features'] = list(filter(
            lambda f: f['properties']['lad11cd'].startswith('E090000'), london_lads['features']))
        with open(london_jsonfile, 'w') as f:
            cd.start_timer()
            json.dump(london_lads, f)
            cd.print_timer('Write london lad GeoJson')  # 4s 2MB
    else:
        with open(london_jsonfile) as f:
            cd.start_timer()
            london_lads = json.load(f)
            cd.print_timer('Read london lad GeoJson')  # 0.07s 2MB
    return london_lads


if __name__ == '__main__':
    london_wards = read_london_ward_geojson()
    london_lads = read_london_lad_geojson()
