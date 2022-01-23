from turtle import width
import geopandas as gpd
import pandas as pd
import geojson_rewind as gr
import plotly.express as px
import json
import os
from plotly.offline import plot
from bokeh.io import output_notebook, show, output_file
from bokeh.plotting import figure
from bokeh.models import GeoJSONDataSource, LinearColorMapper, ColorBar
from bokeh.palettes import brewer


# Get Residence Type data
datafile = "data/BulkdatadetailedcharacteristicsmergedwardspluslaandregE&Wandinfo3.3/DC1104EWDATA.CSV"
# DC1104EW0001	All categories: Age, All categories: Residence type, All categories: Sex
datacol = "DC1104EW0001"
locationcol = "GeographyCode"
columns = [locationcol, datacol]
df = pd.read_csv(datafile, usecols=columns)

# Get Census Merged Ward and Local Authority Data
lookupfile = "data/Ward_to_Census_Merged_Ward_to_Local_Authority_District_(December_2011)_Lookup_in_England_and_Wales.csv"
cmwd = pd.read_csv(lookupfile, usecols=[
                   'CMWD11CD', 'CMWD11NM', 'LAD11CD', 'LAD11NM'])
cmwd.drop_duplicates(inplace=True)
cmwd[locationcol] = cmwd['CMWD11CD']
namecol = 'Name'
cmwd[namecol] = cmwd['CMWD11NM']
lad = pd.read_csv(lookupfile, usecols=['LAD11CD', 'LAD11NM'])
lad[locationcol] = lad['LAD11CD']
lad[namecol] = lad['LAD11NM']
lad['CMWD11CD'] = ''
lad['CMWD11NM'] = ''
geography = pd.concat([cmwd, lad])

# Add names to data
df = pd.merge(df, geography, on=locationcol)

# Get London GeoJSON
london_jsonfile = "data/json_files/London_Ward_Boundaries.json"
if not os.path.exists(london_jsonfile):

    # Census Ward Boundaries as GeoJSON
    census_jsonfile = "data/json_files/Census_Merged_Wards_(December_2011)_Boundaries.json"
    if not os.path.exists(census_jsonfile):

        # Get Census Boundaries as GeoPandas
        shapefile = 'data/Census_Merged_Wards_(December_2011)_Boundaries/Census_Merged_Wards_(December_2011)_Boundaries.shp'
        gdf = gpd.read_file(shapefile)
        # Convert coordinates
        gdf.to_crs(epsg=4326, inplace=True)
        # Write GeoJSON
        gdf.to_file(
            "data/json_files/Census_Merged_Wards_(December_2011)_Boundaries.json", driver='GeoJSON')

    with open(census_jsonfile) as f:
        census_wards = json.load(f)

    lgdf = gdf[gdf['lad11cd'].str.match('E090000')]
    lgdf.to_file(london_jsonfile, driver='GeoJSON')

with open(london_jsonfile) as f:
    london_wards = json.load(f)

# Get London Data
london_ward_ids = list(map(lambda f: f['properties']
                           ['cmwd11cd'], london_wards["features"]))
#london_ward_ids = ['E36007051', 'E36007052']
london_flags = df[locationcol].isin(london_ward_ids)
ldf = df[london_flags]

# No longer necessary?
# london_wards_corrected = gr.rewind(london_wards, rfc7946=False)
max_value = ldf[datacol].max()
fig = px.choropleth(ldf,
                    geojson=london_wards,  # Was london_wards_corrected
                    locations=locationcol,
                    color=datacol,
                    color_continuous_scale="Viridis",
                    range_color=(0, max_value),
                    featureidkey="properties.cmwd11cd",
                    scope='europe',
                    # projection="merc,ator",
                    # customdata=ldf[namecol],
                    # hovertemplate='<br>x:%{x}<br>y:%{y}<br>z:%{z}<br>m:%{customdata}'
                    hover_data=[namecol, 'LAD11NM'],
                    title='Title'
                    )
fig.update_geos(fitbounds="geojson", visible=False, framewidth=1000)
fig.update_layout(margin=dict(l=0, r=0, b=0, t=30),
                  title_x=0.5,
                  width=1500)
# fig.show()
plot(fig)
fig.write_html(('html_files/london_wards.html'))
