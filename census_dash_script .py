import plotly.graph_objects as go
from functools import reduce
from dash.dependencies import Input, Output
from dash import html
from dash import dcc
import dash
import geopandas as gpd
import pandas as pd
import plotly.express as px
import json
import os
from turfpy.measurement import bbox

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
lad = lad.drop_duplicates()
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

# Get LAD GeoJSON
london_jsonfile = "data/json_files/London_LAD_Boundaries.json"
if not os.path.exists(london_jsonfile):

    lad_jsonfile = "data/json_files/Local_Authority_Districts_(December_2011)_Boundaries_EW_BFC.json"
    if not os.path.exists(lad_jsonfile):

        # Get Census LAD Boundaries as GeoPandas
        shapefile = 'data/Local_Authority_Districts_(December_2011)_Boundaries_EW_BFC/Local_Authority_Districts_(December_2011)_Boundaries_EW_BFC.shp'
        ladgdf = gpd.read_file(shapefile)
        # Convert coordinates
        ladgdf.to_crs(epsg=4326, inplace=True)
        # Write GeoJSON
        ladgdf.to_file(lad_jsonfile, driver='GeoJSON')

    with open(lad_jsonfile) as f:
        census_lads = json.load(f)

    lladgdf = ladgdf[ladgdf['lad11cd'].str.match('E090000')]
    lladgdf.to_file(london_jsonfile, driver='GeoJSON')

with open(london_jsonfile) as f:
    london_lads = json.load(f)

# Get London Data
london_ward_ids = list(map(lambda f: f['properties']
                           ['cmwd11cd'], london_wards["features"]))
#london_ward_ids = ['E36007051', 'E36007052']
london_flags = df[locationcol].isin(london_ward_ids)
ldf = df[london_flags]
ward_max_value = ldf[datacol].max()

london_lad_ids = list(map(lambda f: f['properties']
                          ['lad11cd'], london_lads["features"]))
#london_lad_ids = ['E36007051', 'E36007052']
london_flags = df[locationcol].isin(london_lad_ids)
lladdf = df[london_flags]
lad_max_value = lladdf[datacol].max()

# Dash


def blank_fig():
    fig = go.Figure(go.Scatter(x=[], y=[]))
    fig.update_layout(template=None)
    fig.update_xaxes(showgrid=False, showticklabels=False, zeroline=False)
    fig.update_yaxes(showgrid=False, showticklabels=False, zeroline=False)
    return fig


app = dash.Dash(__name__)

local_authorities = pd.Series(ldf['LAD11CD'].unique())
all_local_authorities = pd.concat([pd.Series(['All']), local_authorities])

app.layout = html.Div([
    html.Div([

        html.Div([
            dcc.RadioItems(
                id='granularity',
                options=[{'label': i, 'value': i}
                         for i in ['Ward', 'Local Authority']],
                value='Ward',
                #labelStyle={'display': 'inline-block'},
                style=dict(
                    width='40%',
                    verticalAlign="middle",
                    fontSize='large'
                )
            ),
            html.Label('Local Authority', style={
                       'margin-right': '2em', 'font-size': 'large'}),
            dcc.Dropdown(
                id='local-authority',
                options=[
                    #{'label': i, 'value': i}
                    {'label': 'All' if i == 'All'
                     else geography[geography[locationcol] == i][namecol].iat[0],
                     'value': i}
                    for i in all_local_authorities],
                style=dict(
                    width='40%',
                    verticalAlign="middle"
                ),
                value='All'
            )

        ], style={'width': '48%', 'display': 'flex'}),
    ]),

    dcc.Graph(id='map', figure=blank_fig()),

    # dcc.Slider(
    #     id='year--slider',
    #     min=df['Year'].min(),
    #     max=df['Year'].max(),
    #     value=df['Year'].max(),
    #     marks={str(year): str(year) for year in df['Year'].unique()},
    #     step=None
    # )
])


@app.callback(
    Output('map', 'figure'),
    Input('local-authority', 'value'),
    Input('granularity', 'value'),
    # Input('year--slider', 'value')
)
def update_graph(local_authority, granularity):
    print("local_authority="+local_authority)
    print("granularity="+granularity)
    if granularity == 'Local Authority':
        fdf = lladdf
        gj = london_lads
        key = "properties.lad11cd"
        max_value = lad_max_value
        title = datacol + " by Local Authority"
    else:
        key = "properties.cmwd11cd"
        max_value = ward_max_value
        if local_authority == 'All':
            fdf = ldf
            gj = london_wards
            title = datacol + " by Ward"
        else:
            fdf = ldf[ldf['LAD11CD'].str.match(local_authority)]
            gj = {
                'features': list(filter(lambda f: f['properties']['lad11cd'] == local_authority,
                                        london_wards["features"])),
                'type': london_wards['type'],
                'crs': london_wards['crs']
            }
            title = datacol + " by Ward for Local Authority"

    def compute_bbox(gj):
        gj_bbox_list = list(
            map(lambda f: bbox(f['geometry']), gj['features']))
        gj_bbox = reduce(
            lambda b1, b2: [min(b1[0], b2[0]), min(b1[1], b2[1]),
                            max(b1[2], b2[2]), max(b1[3], b2[3])],
            gj_bbox_list)
        return gj_bbox

    gj_bbox = compute_bbox(gj)

    fig = px.choropleth(fdf,
                        geojson=gj,
                        locations=locationcol,
                        color=datacol,
                        color_continuous_scale="Viridis",
                        range_color=(0, max_value),
                        featureidkey=key,
                        scope='europe',
                        hover_data=[namecol, 'LAD11NM'],
                        title=title
                        )
    fig.update_geos(
        # fitbounds="locations",
        center_lon=(gj_bbox[0]+gj_bbox[2])/2.0,
        center_lat=(gj_bbox[1]+gj_bbox[3])/2.0,
        lonaxis_range=[gj_bbox[0], gj_bbox[2]],
        lataxis_range=[gj_bbox[1], gj_bbox[3]],
        visible=False,
    )
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=30),
                      title_x=0.5,
                      width=1500, height=800)
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
