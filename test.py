import pandas as pd
import plotly.express as px
from plotly.offline import plot
from geojson_rewind import rewind

data = [['E36007051', 1465], ['E36007052', 1434]]
locationcol = 'cmwd11cd'
datacol = 'DC1104EW0001'
lldf = pd.DataFrame(data, columns=[locationcol, datacol])

ward = {"type": "FeatureCollection", "features": [
    {"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [[[532097.1003999999, 182012.79949999973], [532083.3992999997, 181949.99960000068], [532136.3995000003, 181623.49929999933], [532116.3004000001, 181579.1007000003], [532070.6995999999, 181572.20099999942], [532026.4996999996, 181530.49960000068], [532037.8005999997, 181453.09950000048], [532038.4006000003, 181400.09930000082], [532016.3006999996, 181352.20069999993], [532025.5003000004, 181319.89970000088], [532118.6003, 181285.8004999999], [532160.1993000004, 181241.29949999973], [532211.3992999997, 181220.20099999942], [532435.4995999997, 181167.49980000034], [532553.4993000003, 181141.8998000007], [532590.0991000002, 181285.90080000088], [532553.4009999996, 181291.1007000003], [532556.8005999997, 181336.9001000002], [532494.6008000001, 181337.99990000017], [532496.9007000001, 181382.79990000091], [532469.1995000001, 181394.7991000004], [
        532431.9995999997, 181314.40080000088], [532400.2002999997, 181336.40240000002], [532207.2008999996, 181402.30089999922], [532248.9002, 181562.99929999933], [532277.2998000002, 181637.8004999999], [532249.2995999996, 181655.60170000046], [532269.4007000001, 181713.59899999946], [532251.0998, 181719.99899999984], [532269.5993999997, 181775.00009999983], [532284.7995999996, 181769.8002000004], [532305.4003999997, 181819.59940000065], [532295.0006999997, 181829.90289999917], [532308.9005000005, 181914.80269999988], [532152.5009000003, 181864.4997000005], [532131.2999999998, 181930.69930000044], [532116.2001, 182012.69910000078], [532097.1003999999, 182012.79949999973]]]}, "properties":{"objectid": 7051, "cmwd11cd": "E36007051", "cmwd11nm": "Aldersgate,Cheap", "cmwd11nmw": "None", "lad11cd": "E09000001", "lad11nm": "City of London", "lad11nmw": "None", "st_areasha": 175438.448590975, "st_lengths": 3057.1534952154802}},
    {"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [[[533378.8003000002, 181881.69879999943], [533394.1009, 181985.10029999912], [533410.6999000004, 182037.90179999918], [533320.2007999998, 182053.3990000002], [533230.5005000001, 182082.49909999967], [533215.7999, 182024.1004000008], [533184.6007000003, 181948.20150000043], [533146.8008000003, 181897.90059999935], [533078.8992999997, 181840.4991999995], [532946.1009, 181894.90020000003], [532880.4993000003, 181723.40069999918], [532971.5001999997, 181678.6007000003], [533034.9001000002, 181652.80000000075], [532928.1009999998, 181502.7982999999], [532789.8979000002, 181532.8998000007], [532771.0992999999, 181369.10080000013], [532674.2001999998, 181372.60080000013], [532665.3998999996, 181331.80059999973], [532697.7993000001, 181327.2991000004], [532703.7999, 181263.49980000034], [532785.6995000001, 181258.90000000037], [532900.3997, 181290.19959999993], [532942.7012, 181283.29979999922], [532897.6001000004, 181215.1997999996], [532880.7000000002, 181200.4009000007], [532826.1003, 181180.69910000078], [532726.801, 181132.10219999962], [532716.4995999997, 181101.79990000091], [532766.4994999999, 181014.89919999987], [532730.9994000001, 180947.9991999995], [532744.4998000003, 180940.59979999997], [532749.4989999998, 180879.39939999953], [532778.4003999997, 180871.39990000054], [532750.7994999997, 180793.3998000007], [532785.0993999997, 180781.19989999942], [532773.3009000001, 180749.19989999942], [532721.5991000002, 180518.40049999952], [532806.5971999997, 180505.5985000003], [532985.0005999999, 180488.89910000004], [533072.4993000003, 180467.70020000078], [533213.1007000003, 180439.5996000003], [
        533334.2010000004, 180406.7006000001], [533360.4993000003, 180486.90020000003], [533396.9005000005, 180522.2979000006], [533409.0000999998, 180580.3995999992], [533430.3996000001, 180627.1001999993], [533412.7991000004, 180659.39919999987], [533417.4993000003, 180691.79849999957], [533442.9006000003, 180695.99899999984], [533465.7993000001, 180745.3004999999], [533505.8028999995, 180778.69930000044], [533551.3995000003, 180784.4991999995], [533552.2002999997, 180816.90059999935], [533594.3973000003, 180822.39949999936], [533609.8003000002, 180774.09950000048], [533630.5998, 180777.09979999997], [533645.4007000001, 180735.40049999952], [533696.699, 180763.9003999997], [533725.5, 180759.30059999973], [533765.9008999998, 180776.8007999994], [533824.2995999996, 180779.6004000008], [533839.6003, 180808.39939999953], [533832.8009000001, 180888.79979999922], [533815.9990999997, 180954.90100000054], [533796.7991000004, 181094.90020000003], [533765.8005999997, 181226.09919999912], [533743.7006000001, 181261.40059999935], [533659.4008, 181359.39939999953], [533567.4006000003, 181457.50070000067], [533532.5005999999, 181506.59940000065], [533448.8991999999, 181702.29810000025], [533445.1002000002, 181755.9003999997], [533352.0000999998, 181739.79900000058], [533378.8003000002, 181881.69879999943]]]}, "properties":{"objectid": 7052, "cmwd11cd": "E36007052", "cmwd11nm": "Aldgate,Billingsgate,Bishopsgate,Bridge,Broad Street,Candlewick,Cornhill,Langbourn,Lime Street,Portsoken,Tower", "cmwd11nmw": "None", "lad11cd": "E09000001", "lad11nm": "City of London", "lad11nmw": "None", "st_areasha": 1141794.52245595, "st_lengths": 6002.379226322833}}
]}
ward_corrected = rewind(ward, rfc7946=False)

max_value = lldf[datacol].max()
fig = px.choropleth(lldf, geojson=ward_corrected, locations=locationcol,
                    color=datacol,
                    color_continuous_scale="Viridis",
                    range_color=(0, max_value),
                    featureidkey="properties.cmwd11cd",
                    scope='europe',
                    projection="mercator"
                    )
fig.update_geos(
    # fitbounds="locations",
    lataxis_range=[530000, 540000],
    lonaxis_range=[180000, 182000],
    visible=False
)
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
# fig.show()
plot(fig)