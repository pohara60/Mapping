import census_read_data as crd
import census_read_geojson as crg
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from dash import html
from dash import dcc
import dash
from turfpy.measurement import bbox
from functools import reduce

# Get Residence Type data
# DC1104EW0001	All categories: Age, All categories: Residence type, All categories: Sex
index = crd.read_index()
print(index.head())
table_name = index['Table Number'][0]
tdf = crd.read_table(table_name)
data_name = tdf['Dataset'][0]
df = crd.read_data(table_name)
datacol = df.columns[1]

# Get Census Merged Ward and Local Authority Data
geography = crd.read_geography()
locationcol = "GeographyCode"
namecol = "Name"

# Add names to data
df = pd.merge(df, geography, on=locationcol)

# Get London GeoJSON
london_wards = crg.read_london_ward_geojson()

# Get LAD GeoJSON
london_lads = crg.read_london_lad_geojson()

# Filter London Data
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

# Blank figure for initial Dash display


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
