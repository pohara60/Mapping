import census_debug as cd
import geopandas as gpd
import pandas
import os


def read_london_ward_geopandas():

    # Get Census Boundaries as GeoPandas
    shapefile = 'data/Census_Merged_Wards_(December_2011)_Boundaries/Census_Merged_Wards_(December_2011)_Boundaries.shp'
    cd.start_timer()
    gdf = gpd.read_file(shapefile)
    # Convert coordinates
    gdf.to_crs(epsg=4326, inplace=True)
    cd.print_timer('Read ward shapefile')      # 2s 122MB

    # London
    lgdf = gdf[gdf['lad11cd'].str.startswith('E090000')]
    return lgdf


def read_london_lad_geopandas():

    # Get Local Authority Boundaries as GeoPandas
    shapefile = 'data/Local_Authority_Districts_(December_2011)_Boundaries_EW_BFC/Local_Authority_Districts_(December_2011)_Boundaries_EW_BFC.shp'
    cd.start_timer()
    gdf = gpd.read_file(shapefile)
    # Convert coordinates
    gdf.to_crs(epsg=4326, inplace=True)
    cd.print_timer('Read lad shapefile')      # 2s 122MB

    # London
    ladgdf = gdf[gdf['lad11cd'].str.startswith('E090000')]
    return ladgdf


if __name__ == '__main__':
    london_wards_gdf = read_london_ward_geopandas()
    print(london_wards_gdf.head())
    london_lads_gdf = read_london_lad_geopandas()
    print(london_lads_gdf.head())
