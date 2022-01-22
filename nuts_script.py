from geojson_rewind import rewind
import plotly.express as px
from plotly.offline import plot
import pandas as pd
import json
from urllib.request import urlopen
import numpy as np

# Load GeoJson
with urlopen('https://opendata.arcgis.com/datasets/48b6b85bb7ea43699ee85f4ecd12fd36_4.geojson') as response:
    counties = json.load(response)

# Load data to be charted
dummy_data = pd.read_csv(
    'https://opendata.arcgis.com/datasets/48b6b85bb7ea43699ee85f4ecd12fd36_0.csv?outSR=%7B%22latestWkid%22%3A27700%2C%22wkid%22%3A27700%7D')
# add dummy data
dummy_data['value'] = np.random.randint(10, 100, size=len(dummy_data))

# With Plotly

# Make the rings clockwwise (to make it compatible with plotly)
counties_corrected = rewind(counties, rfc7946=False)

fig = px.choropleth(dummy_data, geojson=counties_corrected, locations='nuts218cd', featureidkey="properties.nuts218cd", color='value',
                    color_continuous_scale="PurPor", labels={'label name': 'label name'}, title='MAP TITLE',
                    scope="europe")

fig.update_geos(fitbounds="locations", visible=False)
plot(fig)
fig.write_html(('html_files/nuts.html'))
