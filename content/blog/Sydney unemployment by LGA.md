Title: Which Sydney LGAs have the lowest and highest unemployment rates?
Date: 2023-11-16
Description: Visualising on a Choropleth map Sydney's unemployment rate by local government area, based on Australian government data from Jobs and Skills Australia.
Tags: data-analysis, data-visualisation, Python, pandas

<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-TFP90633KX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-TFP90633KX');
</script>

The Australian government's [Jobs and Skills Australia](https://www.jobsandskills.gov.au/engage/about) has an insightful [dataset](https://www.jobsandskills.gov.au/data/small-area-labour-markets) I recently came across - quarterly Small Area Labour Markets (SALM) estimates of unemployment and the unemployment rate, broken out by local government area (LGA).

Here it is visualised:

<div class="iframe-container">
<iframe src="https://ben-nour.com/sydney_unemployment.html" height="500" width="750"></iframe>
</div>

You can interact with the hosted map [here](https://ben-nour.com/sydney_unemployment.html).

## How I did it

I sourced a [GeoJSON file](https://citydata.be.unsw.edu.au/dataset/lgas_sydney_and_surrounds/resource/75080649-cd92-4923-bf71-63c81e5c57ba) of Greater Sydney LGAs from UNSW's [CityData](https://citydata.be.unsw.edu.au/) platform.


```python
import folium
import requests
import pandas as pd

response = requests.get("https://staging.citydata.be.unsw.edu.au/geoserver/geonode/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=geonode:LGAs_Sydney_and_surrounds&outputFormat=application%2Fjson")
geojson = response.json()
```

There was some typical data cleaning that I needed to apply to the unemployment dataset (making more readable column headers, converting the data type).


```python
df = pd.read_csv('unemployment.csv')
df = df[['Data item', 'Local Government Area (LGA) (2023 ASGS)', 'Jun-23']]
df = df.query("`Data item` == 'Smoothed unemployment rate (%)'")
df = df.rename(columns={'Local Government Area (LGA) (2023 ASGS)':'LGA', 'Jun-23':'unemployment_rate'})
df['unemployment_rate'] = pd.to_numeric(df['unemployment_rate'], errors='coerce')
```

But the big issue was that unfortunately not all the LGA names in the CSV matched the LGA names in the GeoJSON file so I had manually updated these records to reflect the naming used in the GeoJSON file.


```python
# Printing the names of the LGAs in the GeoJSON file.
lgas = []
for number in range(0, len(geojson['features'])):
    lga = geojson['features'][number]['properties']['NSW_LGA__3']
    lgas.append(lga)

lgas = list(set(lgas))
geojson_lgas = pd.Series(lgas)
geojson_lgas.name = 'LGA'
geojson_lgas
```




    0         SUTHERLAND SHIRE
    1                  BURWOOD
    2                LANE COVE
    3               WILLOUGHBY
    4               INNER WEST
    5              STRATHFIELD
    6               CUMBERLAND
    7           UNINCORPORATED
    8                 WAVERLEY
    9                  BAYSIDE
    10              HAWKESBURY
    11                  CAMDEN
    12             WOLLONDILLY
    13            CAMPBELLTOWN
    14               LIVERPOOL
    15          BLUE MOUNTAINS
    16               FAIRFIELD
    17             KU-RING-GAI
    18              CANADA BAY
    19                 PENRITH
    20                 HORNSBY
    21                    RYDE
    22         THE HILLS SHIRE
    23                  SYDNEY
    24           CENTRAL COAST
    25        NORTHERN BEACHES
    26    CANTERBURY-BANKSTOWN
    27            NORTH SYDNEY
    28            HUNTERS HILL
    29                  MOSMAN
    30                RANDWICK
    31               BLACKTOWN
    32           GEORGES RIVER
    33               WOOLLAHRA
    34              PARRAMATTA
    Name: LGA, dtype: object




```python
# Updating LGA names in the unemployment DataFrame.
df['LGA'] = df['LGA'].str.upper()
df.at[1107, 'LGA'] = 'CAMPBELLTOWN'
df.at[1195, 'LGA'] = 'THE HILLS SHIRE'
df.at[1091, 'LGA'] = 'BAYSIDE'
df.at[1190, 'LGA'] = 'SUTHERLAND SHIRE'
df.at[1111, 'LGA'] = 'CENTRAL COAST'

df
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Data item</th>
      <th>LGA</th>
      <th>unemployment_rate</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1086</th>
      <td>Smoothed unemployment rate (%)</td>
      <td>ALBURY</td>
      <td>4.5</td>
    </tr>
    <tr>
      <th>1087</th>
      <td>Smoothed unemployment rate (%)</td>
      <td>ARMIDALE</td>
      <td>2.8</td>
    </tr>
    <tr>
      <th>1088</th>
      <td>Smoothed unemployment rate (%)</td>
      <td>BALLINA</td>
      <td>1.7</td>
    </tr>
    <tr>
      <th>1089</th>
      <td>Smoothed unemployment rate (%)</td>
      <td>BALRANALD</td>
      <td>1.8</td>
    </tr>
    <tr>
      <th>1090</th>
      <td>Smoothed unemployment rate (%)</td>
      <td>BATHURST</td>
      <td>1.6</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>1624</th>
      <td>Smoothed unemployment rate (%)</td>
      <td>WAGAIT</td>
      <td>2.3</td>
    </tr>
    <tr>
      <th>1625</th>
      <td>Smoothed unemployment rate (%)</td>
      <td>WEST ARNHEM</td>
      <td>9.3</td>
    </tr>
    <tr>
      <th>1626</th>
      <td>Smoothed unemployment rate (%)</td>
      <td>WEST DALY</td>
      <td>13.0</td>
    </tr>
    <tr>
      <th>1627</th>
      <td>Smoothed unemployment rate (%)</td>
      <td>UNINCORPORATED NT</td>
      <td>5.2</td>
    </tr>
    <tr>
      <th>1628</th>
      <td>Smoothed unemployment rate (%)</td>
      <td>UNINCORPORATED ACT</td>
      <td>3.0</td>
    </tr>
  </tbody>
</table>
<p>543 rows × 3 columns</p>
</div>



I also needed to modify and recreate the GeoJSON file, to:

- Add the unemployment rate to the properties of each Feature so the data can be passed to a tooltip popup in the map.

- Remove suburbs not in Greater Sydney (this dataset includes surrounding LGAs like Hawkesbury and Central Coast).



```python
# Setting the index on the unemployment DataFrame to LGA in order to pass the unemployment rate
# to the GeoJSON properties.
df['LGA_index'] = df['LGA']
df = df.set_index('LGA_index')

new_geojson = {'type':'FeatureCollection'}
# Creating a new GeoJSON file consisiting of only Greater Sydney suburbs
# and adding unemployment_rate to the Feature properties.
features = []
for feature in geojson['features']:
    if feature['properties']['NSW_LGA__3'] not in ('UNINCORPORATED', 'CENTRAL COAST', 'BLUE MOUNTAINS', 'WOLLONDILLY', 'HAWKESBURY'):
        feature_lga = feature['properties']['NSW_LGA__3']
        try:
            unemployment_rate = df.at[feature_lga, 'unemployment_rate']
            unemployment_rate = str(unemployment_rate) + '%'
            feature['properties']['unemployment_rate'] = unemployment_rate
            features.append(feature)
        except KeyError:
            pass
new_geojson['features'] = features

lgas = []
for number in range(0, len(new_geojson['features'])):
    lga = new_geojson['features'][number]['properties']['NSW_LGA__3']
    lgas.append(lga)

# Creating a Series object from the new GeoJSON file.
lgas = list(set(lgas))
geojson_lgas = pd.Series(lgas)
geojson_lgas.name = 'LGA'
```

Finally I just had to inner join the two DataFrames to filter out LGAs that aren't in Sydney and then I could create the map!


```python
sydney_lgas_unemployment = pd.merge(geojson_lgas, df, left_on="LGA", right_on="LGA")
```


```python
m = folium.Map(location=[-33.8688, 151.2093], zoom_start=9.5)

choropleth = folium.Choropleth(
    geo_data=new_geojson,
    data=sydney_lgas_unemployment,
    columns=["LGA", "unemployment_rate"],
    key_on="feature.properties.NSW_LGA__3",
    fill_opacity=0.7,
    line_weight=2,
    fill_color="YlOrRd",
    highlight=True,
    legend_name="Unemployment rate %"
).add_to(m)

tooltip = folium.GeoJsonTooltip(fields=["NSW_LGA__3", "unemployment_rate"], aliases=["LGA", "Unemployment rate"])
choropleth.geojson.add_child(tooltip)

m.save('sydney_unemployment.html')
m
```




<div style="width:100%;"><div style="position:relative;width:100%;height:0;padding-bottom:60%;"><span style="color:#565656">Make this Notebook Trusted to load map: File -> Trust Notebook</span><iframe srcdoc="&lt;!DOCTYPE html&gt;
&lt;html&gt;
&lt;head&gt;

    &lt;meta http-equiv=&quot;content-type&quot; content=&quot;text/html; charset=UTF-8&quot; /&gt;

        &lt;script&gt;
            L_NO_TOUCH = false;
            L_DISABLE_3D = false;
        &lt;/script&gt;

    &lt;style&gt;html, body {width: 100%;height: 100%;margin: 0;padding: 0;}&lt;/style&gt;
    &lt;style&gt;#map {position:absolute;top:0;bottom:0;right:0;left:0;}&lt;/style&gt;
    &lt;script src=&quot;https://cdn.jsdelivr.net/npm/leaflet@1.9.3/dist/leaflet.js&quot;&gt;&lt;/script&gt;
    &lt;script src=&quot;https://code.jquery.com/jquery-3.7.1.min.js&quot;&gt;&lt;/script&gt;
    &lt;script src=&quot;https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/js/bootstrap.bundle.min.js&quot;&gt;&lt;/script&gt;
    &lt;script src=&quot;https://cdnjs.cloudflare.com/ajax/libs/Leaflet.awesome-markers/2.0.2/leaflet.awesome-markers.js&quot;&gt;&lt;/script&gt;
    &lt;link rel=&quot;stylesheet&quot; href=&quot;https://cdn.jsdelivr.net/npm/leaflet@1.9.3/dist/leaflet.css&quot;/&gt;
    &lt;link rel=&quot;stylesheet&quot; href=&quot;https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/css/bootstrap.min.css&quot;/&gt;
    &lt;link rel=&quot;stylesheet&quot; href=&quot;https://netdna.bootstrapcdn.com/bootstrap/3.0.0/css/bootstrap.min.css&quot;/&gt;
    &lt;link rel=&quot;stylesheet&quot; href=&quot;https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@6.2.0/css/all.min.css&quot;/&gt;
    &lt;link rel=&quot;stylesheet&quot; href=&quot;https://cdnjs.cloudflare.com/ajax/libs/Leaflet.awesome-markers/2.0.2/leaflet.awesome-markers.css&quot;/&gt;
    &lt;link rel=&quot;stylesheet&quot; href=&quot;https://cdn.jsdelivr.net/gh/python-visualization/folium/folium/templates/leaflet.awesome.rotate.min.css&quot;/&gt;

            &lt;meta name=&quot;viewport&quot; content=&quot;width=device-width,
                initial-scale=1.0, maximum-scale=1.0, user-scalable=no&quot; /&gt;
            &lt;style&gt;
                #map_9acbafbc0805ac35fc08414fa62c4426 {
                    position: relative;
                    width: 100.0%;
                    height: 100.0%;
                    left: 0.0%;
                    top: 0.0%;
                }
                .leaflet-container { font-size: 1rem; }
            &lt;/style&gt;


                    &lt;style&gt;
                        .foliumtooltip {

                        }
                       .foliumtooltip table{
                            margin: auto;
                        }
                        .foliumtooltip tr{
                            text-align: left;
                        }
                        .foliumtooltip th{
                            padding: 2px; padding-right: 8px;
                        }
                    &lt;/style&gt;

    &lt;script src=&quot;https://cdnjs.cloudflare.com/ajax/libs/d3/3.5.5/d3.min.js&quot;&gt;&lt;/script&gt;
&lt;/head&gt;
&lt;body&gt;


            &lt;div class=&quot;folium-map&quot; id=&quot;map_9acbafbc0805ac35fc08414fa62c4426&quot; &gt;&lt;/div&gt;

&lt;/body&gt;
&lt;script&gt;


            var map_9acbafbc0805ac35fc08414fa62c4426 = L.map(
                &quot;map_9acbafbc0805ac35fc08414fa62c4426&quot;,
                {
                    center: [-33.8688, 151.2093],
                    crs: L.CRS.EPSG3857,
                    zoom: 9.5,
                    zoomControl: true,
                    preferCanvas: false,
                }
            );





            var tile_layer_5a43d4994b4ad4cf419542b0490bd526 = L.tileLayer(
                &quot;https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png&quot;,
                {&quot;attribution&quot;: &quot;Data by \u0026copy; \u003ca target=\&quot;_blank\&quot; href=\&quot;http://openstreetmap.org\&quot;\u003eOpenStreetMap\u003c/a\u003e, under \u003ca target=\&quot;_blank\&quot; href=\&quot;http://www.openstreetmap.org/copyright\&quot;\u003eODbL\u003c/a\u003e.&quot;, &quot;detectRetina&quot;: false, &quot;maxNativeZoom&quot;: 18, &quot;maxZoom&quot;: 18, &quot;minZoom&quot;: 0, &quot;noWrap&quot;: false, &quot;opacity&quot;: 1, &quot;subdomains&quot;: &quot;abc&quot;, &quot;tms&quot;: false}
            );


                tile_layer_5a43d4994b4ad4cf419542b0490bd526.addTo(map_9acbafbc0805ac35fc08414fa62c4426);

            var choropleth_7166844dd7229e547513835f2a28ea67 = L.featureGroup(
                {}
            );


        function geo_json_897666aa07644781ee99eb2512ea01d6_styler(feature) {
            switch(feature.id) {
                case &quot;LGAs_Sydney_and_surrounds.1&quot;: case &quot;LGAs_Sydney_and_surrounds.11&quot;: case &quot;LGAs_Sydney_and_surrounds.20&quot;: case &quot;LGAs_Sydney_and_surrounds.22&quot;: case &quot;LGAs_Sydney_and_surrounds.31&quot;: case &quot;LGAs_Sydney_and_surrounds.35&quot;: 
                    return {&quot;color&quot;: &quot;black&quot;, &quot;fillColor&quot;: &quot;#feb24c&quot;, &quot;fillOpacity&quot;: 0.7, &quot;opacity&quot;: 1, &quot;weight&quot;: 2};
                case &quot;LGAs_Sydney_and_surrounds.2&quot;: case &quot;LGAs_Sydney_and_surrounds.6&quot;: case &quot;LGAs_Sydney_and_surrounds.8&quot;: case &quot;LGAs_Sydney_and_surrounds.13&quot;: case &quot;LGAs_Sydney_and_surrounds.15&quot;: case &quot;LGAs_Sydney_and_surrounds.21&quot;: case &quot;LGAs_Sydney_and_surrounds.23&quot;: case &quot;LGAs_Sydney_and_surrounds.24&quot;: case &quot;LGAs_Sydney_and_surrounds.25&quot;: case &quot;LGAs_Sydney_and_surrounds.28&quot;: case &quot;LGAs_Sydney_and_surrounds.32&quot;: case &quot;LGAs_Sydney_and_surrounds.33&quot;: case &quot;LGAs_Sydney_and_surrounds.34&quot;: case &quot;LGAs_Sydney_and_surrounds.36&quot;: 
                    return {&quot;color&quot;: &quot;black&quot;, &quot;fillColor&quot;: &quot;#ffffb2&quot;, &quot;fillOpacity&quot;: 0.7, &quot;opacity&quot;: 1, &quot;weight&quot;: 2};
                case &quot;LGAs_Sydney_and_surrounds.18&quot;: case &quot;LGAs_Sydney_and_surrounds.19&quot;: case &quot;LGAs_Sydney_and_surrounds.27&quot;: case &quot;LGAs_Sydney_and_surrounds.29&quot;: 
                    return {&quot;color&quot;: &quot;black&quot;, &quot;fillColor&quot;: &quot;#fd8d3c&quot;, &quot;fillOpacity&quot;: 0.7, &quot;opacity&quot;: 1, &quot;weight&quot;: 2};
                case &quot;LGAs_Sydney_and_surrounds.26&quot;: 
                    return {&quot;color&quot;: &quot;black&quot;, &quot;fillColor&quot;: &quot;#bd0026&quot;, &quot;fillOpacity&quot;: 0.7, &quot;opacity&quot;: 1, &quot;weight&quot;: 2};
                default:
                    return {&quot;color&quot;: &quot;black&quot;, &quot;fillColor&quot;: &quot;#fed976&quot;, &quot;fillOpacity&quot;: 0.7, &quot;opacity&quot;: 1, &quot;weight&quot;: 2};
            }
        }
        function geo_json_897666aa07644781ee99eb2512ea01d6_highlighter(feature) {
            switch(feature.id) {
                default:
                    return {&quot;fillOpacity&quot;: 0.8999999999999999, &quot;weight&quot;: 4};
            }
        }

        function geo_json_897666aa07644781ee99eb2512ea01d6_onEachFeature(feature, layer) {
            layer.on({
                mouseout: function(e) {
                    if(typeof e.target.setStyle === &quot;function&quot;){
                        geo_json_897666aa07644781ee99eb2512ea01d6.resetStyle(e.target);
                    }
                },
                mouseover: function(e) {
                    if(typeof e.target.setStyle === &quot;function&quot;){
                        const highlightStyle = geo_json_897666aa07644781ee99eb2512ea01d6_highlighter(e.target.feature)
                        e.target.setStyle(highlightStyle);
                    }
                },
            });
        };
        var geo_json_897666aa07644781ee99eb2512ea01d6 = L.geoJson(null, {
                onEachFeature: geo_json_897666aa07644781ee99eb2512ea01d6_onEachFeature,

                style: geo_json_897666aa07644781ee99eb2512ea01d6_styler,
        });

        function geo_json_897666aa07644781ee99eb2512ea01d6_add (data) {
            geo_json_897666aa07644781ee99eb2512ea01d6
                .addData(data);
        }



    geo_json_897666aa07644781ee99eb2512ea01d6.bindTooltip(
    function(layer){
    let div = L.DomUtil.create(&#x27;div&#x27;);

    let handleObject = feature=&gt;typeof(feature)==&#x27;object&#x27; ? JSON.stringify(feature) : feature;
    let fields = [&quot;NSW_LGA__3&quot;, &quot;unemployment_rate&quot;];
    let aliases = [&quot;LGA&quot;, &quot;Unemployment rate&quot;];
    let table = &#x27;&lt;table&gt;&#x27; +
        String(
        fields.map(
        (v,i)=&gt;
        `&lt;tr&gt;
            &lt;th&gt;${aliases[i]}&lt;/th&gt;

            &lt;td&gt;${handleObject(layer.feature.properties[v])}&lt;/td&gt;
        &lt;/tr&gt;`).join(&#x27;&#x27;))
    +&#x27;&lt;/table&gt;&#x27;;
    div.innerHTML=table;

    return div
    }
    ,{&quot;className&quot;: &quot;foliumtooltip&quot;, &quot;sticky&quot;: true});


                geo_json_897666aa07644781ee99eb2512ea01d6.addTo(choropleth_7166844dd7229e547513835f2a28ea67);

    var color_map_46d3efdc768d9c81e7d1ed947571f2a2 = {};


    color_map_46d3efdc768d9c81e7d1ed947571f2a2.color = d3.scale.threshold()
              .domain([1.7, 1.7110220440881763, 1.7220440881763526, 1.733066132264529, 1.7440881763527054, 1.7551102204408817, 1.766132264529058, 1.7771543086172343, 1.7881763527054109, 1.7991983967935872, 1.8102204408817635, 1.8212424849699398, 1.832264529058116, 1.8432865731462926, 1.854308617234469, 1.8653306613226452, 1.8763527054108216, 1.8873747494989979, 1.8983967935871744, 1.9094188376753507, 1.920440881763527, 1.9314629258517033, 1.9424849699398796, 1.9535070140280562, 1.9645290581162325, 1.9755511022044088, 1.986573146292585, 1.9975951903807614, 2.0086172344689377, 2.019639278557114, 2.0306613226452903, 2.041683366733467, 2.0527054108216434, 2.0637274549098197, 2.074749498997996, 2.0857715430861723, 2.0967935871743486, 2.107815631262525, 2.118837675350701, 2.1298597194388775, 2.1408817635270543, 2.1519038076152306, 2.162925851703407, 2.173947895791583, 2.1849699398797595, 2.195991983967936, 2.207014028056112, 2.2180360721442884, 2.2290581162324647, 2.240080160320641, 2.2511022044088174, 2.2621242484969937, 2.2731462925851704, 2.2841683366733467, 2.295190380761523, 2.3062124248496993, 2.3172344689378757, 2.328256513026052, 2.3392785571142283, 2.350300601202405, 2.3613226452905813, 2.3723446893787576, 2.383366733466934, 2.3943887775551103, 2.4054108216432866, 2.416432865731463, 2.427454909819639, 2.4384769539078155, 2.449498997995992, 2.460521042084168, 2.4715430861723444, 2.4825651302605207, 2.4935871743486975, 2.504609218436874, 2.51563126252505, 2.5266533066132264, 2.5376753507014027, 2.548697394789579, 2.5597194388777553, 2.570741482965932, 2.5817635270541084, 2.5927855711422847, 2.603807615230461, 2.6148296593186373, 2.6258517034068136, 2.63687374749499, 2.6478957915831662, 2.6589178356713425, 2.669939879759519, 2.680961923847695, 2.6919839679358715, 2.7030060120240478, 2.714028056112224, 2.725050100200401, 2.736072144288577, 2.7470941883767535, 2.7581162324649298, 2.769138276553106, 2.780160320641283, 2.791182364729459, 2.8022044088176354, 2.8132264529058117, 2.824248496993988, 2.8352705410821644, 2.8462925851703407, 2.857314629258517, 2.8683366733466933, 2.8793587174348696, 2.890380761523046, 2.901402805611222, 2.9124248496993985, 2.923446893787575, 2.934468937875751, 2.945490981963928, 2.956513026052104, 2.9675350701402805, 2.978557114228457, 2.989579158316633, 3.00060120240481, 3.011623246492986, 3.0226452905811625, 3.033667334669339, 3.044689378757515, 3.0557114228456914, 3.0667334669338677, 3.077755511022044, 3.0887775551102203, 3.0997995991983966, 3.110821643286573, 3.1218436873747493, 3.1328657314629256, 3.143887775551102, 3.154909819639278, 3.165931863727455, 3.1769539078156313, 3.1879759519038076, 3.198997995991984, 3.21002004008016, 3.221042084168337, 3.2320641282565132, 3.2430861723446895, 3.254108216432866, 3.265130260521042, 3.2761523046092185, 3.2871743486973948, 3.298196392785571, 3.3092184368737474, 3.3202404809619237, 3.3312625250501, 3.3422845691382763, 3.3533066132264526, 3.364328657314629, 3.3753507014028052, 3.386372745490982, 3.3973947895791583, 3.4084168336673346, 3.419438877755511, 3.4304609218436872, 3.441482965931864, 3.4525050100200403, 3.4635270541082166, 3.474549098196393, 3.485571142284569, 3.4965931863727455, 3.507615230460922, 3.518637274549098, 3.5296593186372744, 3.5406813627254508, 3.551703406813627, 3.5627254509018034, 3.5737474949899797, 3.584769539078156, 3.5957915831663323, 3.606813627254509, 3.6178356713426854, 3.6288577154308617, 3.639879759519038, 3.6509018036072143, 3.661923847695391, 3.6729458917835673, 3.6839679358717436, 3.69498997995992, 3.7060120240480963, 3.7170340681362726, 3.728056112224449, 3.739078156312625, 3.7501002004008015, 3.761122244488978, 3.772144288577154, 3.7831663326653304, 3.7941883767535067, 3.805210420841683, 3.8162324649298593, 3.8272545090180357, 3.838276553106212, 3.849298597194389, 3.8603206412825655, 3.8713426853707418, 3.882364729458918, 3.8933867735470944, 3.9044088176352707, 3.915430861723447, 3.9264529058116233, 3.9374749498997996, 3.948496993987976, 3.9595190380761522, 3.9705410821643286, 3.981563126252505, 3.992585170340681, 4.0036072144288575, 4.014629258517034, 4.02565130260521, 4.036673346693386, 4.047695390781563, 4.058717434869739, 4.069739478957916, 4.0807615230460925, 4.091783567134269, 4.102805611222445, 4.1138276553106214, 4.124849699398798, 4.135871743486974, 4.14689378757515, 4.157915831663327, 4.168937875751503, 4.179959919839679, 4.190981963927856, 4.202004008016032, 4.213026052104208, 4.2240480961923845, 4.235070140280561, 4.246092184368737, 4.2571142284569135, 4.26813627254509, 4.279158316633266, 4.290180360721443, 4.30120240480962, 4.312224448897796, 4.323246492985972, 4.3342685370741485, 4.345290581162325, 4.356312625250501, 4.367334669338677, 4.378356713426854, 4.38937875751503, 4.400400801603206, 4.411422845691383, 4.422444889779559, 4.433466933867735, 4.444488977955912, 4.455511022044088, 4.466533066132264, 4.4775551102204405, 4.488577154308617, 4.499599198396793, 4.51062124248497, 4.521643286573147, 4.532665330661323, 4.543687374749499, 4.5547094188376755, 4.565731462925852, 4.576753507014028, 4.5877755511022045, 4.598797595190381, 4.609819639278557, 4.620841683366733, 4.63186372745491, 4.642885771543086, 4.653907815631262, 4.664929859719439, 4.675951903807615, 4.686973947895791, 4.697995991983968, 4.709018036072144, 4.72004008016032, 4.731062124248497, 4.742084168336674, 4.75310621242485, 4.764128256513026, 4.775150300601203, 4.786172344689379, 4.797194388777555, 4.8082164328657315, 4.819238476953908, 4.830260521042084, 4.8412825651302605, 4.852304609218437, 4.863326653306613, 4.874348697394789, 4.885370741482966, 4.896392785571142, 4.907414829659318, 4.918436873747495, 4.929458917835671, 4.940480961923847, 4.951503006012024, 4.962525050100201, 4.973547094188377, 4.984569138276553, 4.99559118236473, 5.006613226452906, 5.017635270541082, 5.028657314629259, 5.039679358717435, 5.050701402805611, 5.0617234468937875, 5.072745490981964, 5.08376753507014, 5.094789579158316, 5.105811623246493, 5.116833667334669, 5.127855711422845, 5.138877755511022, 5.149899799599198, 5.160921843687374, 5.1719438877755515, 5.182965931863728, 5.193987975951904, 5.20501002004008, 5.216032064128257, 5.227054108216433, 5.238076152304609, 5.249098196392786, 5.260120240480962, 5.271142284569138, 5.282164328657315, 5.293186372745491, 5.304208416833667, 5.3152304609218435, 5.32625250501002, 5.337274549098196, 5.348296593186372, 5.359318637274549, 5.370340681362725, 5.381362725450901, 5.3923847695390785, 5.403406813627255, 5.414428857715431, 5.4254509018036075, 5.436472945891784, 5.44749498997996, 5.458517034068136, 5.469539078156313, 5.480561122244489, 5.491583166332665, 5.502605210420842, 5.513627254509018, 5.524649298597194, 5.5356713426853705, 5.546693386773547, 5.557715430861723, 5.5687374749498995, 5.579759519038076, 5.590781563126252, 5.601803607214428, 5.612825651302606, 5.623847695390782, 5.634869739478958, 5.6458917835671345, 5.656913827655311, 5.667935871743487, 5.678957915831663, 5.68997995991984, 5.701002004008016, 5.712024048096192, 5.723046092184369, 5.734068136272545, 5.745090180360721, 5.756112224448898, 5.767134268537074, 5.778156312625251, 5.789178356713427, 5.800200400801604, 5.81122244488978, 5.822244488977956, 5.833266533066133, 5.844288577154309, 5.855310621242485, 5.8663326653306616, 5.877354709418838, 5.888376753507014, 5.8993987975951905, 5.910420841683367, 5.921442885771543, 5.932464929859719, 5.943486973947896, 5.954509018036072, 5.965531062124248, 5.976553106212425, 5.987575150300601, 5.998597194388778, 6.0096192384769545, 6.020641282565131, 6.031663326653307, 6.042685370741483, 6.05370741482966, 6.064729458917836, 6.075751503006012, 6.086773547094189, 6.097795591182365, 6.108817635270541, 6.1198396793587175, 6.130861723446894, 6.14188376753507, 6.1529058116232465, 6.163927855711423, 6.174949899799599, 6.185971943887775, 6.196993987975952, 6.208016032064128, 6.219038076152305, 6.2300601202404815, 6.241082164328658, 6.252104208416834, 6.26312625250501, 6.274148296593187, 6.285170340681363, 6.296192384769539, 6.307214428857716, 6.318236472945892, 6.329258517034068, 6.340280561122245, 6.351302605210421, 6.362324649298597, 6.3733466933867735, 6.38436873747495, 6.395390781563126, 6.406412825651302, 6.417434869739479, 6.428456913827655, 6.439478957915832, 6.4505010020040086, 6.461523046092185, 6.472545090180361, 6.4835671342685375, 6.494589178356714, 6.50561122244489, 6.516633266533066, 6.527655310621243, 6.538677354709419, 6.549699398797595, 6.560721442885772, 6.571743486973948, 6.582765531062124, 6.593787575150301, 6.604809619238477, 6.615831663326653, 6.6268537074148295, 6.637875751503006, 6.648897795591182, 6.659919839679359, 6.670941883767536, 6.681963927855712, 6.692985971943888, 6.7040080160320645, 6.715030060120241, 6.726052104208417, 6.7370741482965935, 6.74809619238477, 6.759118236472946, 6.770140280561122, 6.781162324649299, 6.792184368737475, 6.803206412825651, 6.814228456913828, 6.825250501002004, 6.83627254509018, 6.8472945891783565, 6.858316633266533, 6.869338677354709, 6.880360721442886, 6.891382765531063, 6.902404809619239, 6.913426853707415, 6.924448897795592, 6.935470941883768, 6.946492985971944, 6.9575150300601205, 6.968537074148297, 6.979559118236473, 6.990581162324649, 7.001603206412826, 7.012625250501002, 7.023647294589178, 7.034669338677355, 7.045691382765531, 7.056713426853707, 7.067735470941884, 7.07875751503006, 7.089779559118236, 7.100801603206413, 7.11182364729459, 7.122845691382766, 7.133867735470942, 7.144889779559119, 7.155911823647295, 7.166933867735471, 7.177955911823648, 7.188977955911824, 7.2])
              .range([&#x27;#ffffb2ff&#x27;, &#x27;#ffffb2ff&#x27;, &#x27;#ffffb2ff&#x27;, &#x27;#ffffb2ff&#x27;, &#x27;#ffffb2ff&#x27;, &#x27;#ffffb2ff&#x27;, &#x27;#ffffb2ff&#x27;, &#x27;#ffffb2ff&#x27;, &#x27;#ffffb2ff&#x27;, &#x27;#ffffb2ff&#x27;, &#x27;#ffffb2ff&#x27;, &#x27;#ffffb2ff&#x27;, &#x27;#ffffb2ff&#x27;, &#x27;#ffffb2ff&#x27;, &#x27;#ffffb2ff&#x27;, &#x27;#ffffb2ff&#x27;, &#x27;#ffffb2ff&#x27;, &#x27;#ffffb2ff&#x27;, &#x27;#ffffb2ff&#x27;, &#x27;#ffffb2ff&#x27;, &#x27;#ffffb2ff&#x27;, &#x27;#ffffb2ff&#x27;, &#x27;#ffffb2ff&#x27;, &#x27;#ffffb2ff&#x27;, &#x27;#ffffb2ff&#x27;, &#x27;#ffffb2ff&#x27;, &#x27;#ffffb2ff&#x27;, &#x27;#ffffb2ff&#x27;, &#x27;#ffffb2ff&#x27;, &#x27;#ffffb2ff&#x27;, &#x27;#ffffb2ff&#x27;, &#x27;#ffffb2ff&#x27;, &#x27;#ffffb2ff&#x27;, &#x27;#ffffb2ff&#x27;, &#x27;#ffffb2ff&#x27;, &#x27;#ffffb2ff&#x27;, &#x27;#ffffb2ff&#x27;, &#x27;#ffffb2ff&#x27;, &#x27;#ffffb2ff&#x27;, &#x27;#ffffb2ff&#x27;, &#x27;#ffffb2ff&#x27;, &#x27;#ffffb2ff&#x27;, &#x27;#ffffb2ff&#x27;, &#x27;#ffffb2ff&#x27;, &#x27;#ffffb2ff&#x27;, &#x27;#ffffb2ff&#x27;, &#x27;#ffffb2ff&#x27;, &#x27;#ffffb2ff&#x27;, &#x27;#ffffb2ff&#x27;, &#x27;#ffffb2ff&#x27;, &#x27;#ffffb2ff&#x27;, &#x27;#ffffb2ff&#x27;, &#x27;#ffffb2ff&#x27;, &#x27;#ffffb2ff&#x27;, &#x27;#ffffb2ff&#x27;, &#x27;#ffffb2ff&#x27;, &#x27;#ffffb2ff&#x27;, &#x27;#ffffb2ff&#x27;, &#x27;#ffffb2ff&#x27;, &#x27;#ffffb2ff&#x27;, &#x27;#ffffb2ff&#x27;, &#x27;#ffffb2ff&#x27;, &#x27;#ffffb2ff&#x27;, &#x27;#ffffb2ff&#x27;, &#x27;#ffffb2ff&#x27;, &#x27;#ffffb2ff&#x27;, &#x27;#ffffb2ff&#x27;, &#x27;#ffffb2ff&#x27;, &#x27;#ffffb2ff&#x27;, &#x27;#ffffb2ff&#x27;, &#x27;#ffffb2ff&#x27;, &#x27;#ffffb2ff&#x27;, &#x27;#ffffb2ff&#x27;, &#x27;#ffffb2ff&#x27;, &#x27;#ffffb2ff&#x27;, &#x27;#ffffb2ff&#x27;, &#x27;#ffffb2ff&#x27;, &#x27;#ffffb2ff&#x27;, &#x27;#ffffb2ff&#x27;, &#x27;#ffffb2ff&#x27;, &#x27;#ffffb2ff&#x27;, &#x27;#ffffb2ff&#x27;, &#x27;#ffffb2ff&#x27;, &#x27;#ffffb2ff&#x27;, &#x27;#fed976ff&#x27;, &#x27;#fed976ff&#x27;, &#x27;#fed976ff&#x27;, &#x27;#fed976ff&#x27;, &#x27;#fed976ff&#x27;, &#x27;#fed976ff&#x27;, &#x27;#fed976ff&#x27;, &#x27;#fed976ff&#x27;, &#x27;#fed976ff&#x27;, &#x27;#fed976ff&#x27;, &#x27;#fed976ff&#x27;, &#x27;#fed976ff&#x27;, &#x27;#fed976ff&#x27;, &#x27;#fed976ff&#x27;, &#x27;#fed976ff&#x27;, &#x27;#fed976ff&#x27;, &#x27;#fed976ff&#x27;, &#x27;#fed976ff&#x27;, &#x27;#fed976ff&#x27;, &#x27;#fed976ff&#x27;, &#x27;#fed976ff&#x27;, &#x27;#fed976ff&#x27;, &#x27;#fed976ff&#x27;, &#x27;#fed976ff&#x27;, &#x27;#fed976ff&#x27;, &#x27;#fed976ff&#x27;, &#x27;#fed976ff&#x27;, &#x27;#fed976ff&#x27;, &#x27;#fed976ff&#x27;, &#x27;#fed976ff&#x27;, &#x27;#fed976ff&#x27;, &#x27;#fed976ff&#x27;, &#x27;#fed976ff&#x27;, &#x27;#fed976ff&#x27;, &#x27;#fed976ff&#x27;, &#x27;#fed976ff&#x27;, &#x27;#fed976ff&#x27;, &#x27;#fed976ff&#x27;, &#x27;#fed976ff&#x27;, &#x27;#fed976ff&#x27;, &#x27;#fed976ff&#x27;, &#x27;#fed976ff&#x27;, &#x27;#fed976ff&#x27;, &#x27;#fed976ff&#x27;, &#x27;#fed976ff&#x27;, &#x27;#fed976ff&#x27;, &#x27;#fed976ff&#x27;, &#x27;#fed976ff&#x27;, &#x27;#fed976ff&#x27;, &#x27;#fed976ff&#x27;, &#x27;#fed976ff&#x27;, &#x27;#fed976ff&#x27;, &#x27;#fed976ff&#x27;, &#x27;#fed976ff&#x27;, &#x27;#fed976ff&#x27;, &#x27;#fed976ff&#x27;, &#x27;#fed976ff&#x27;, &#x27;#fed976ff&#x27;, &#x27;#fed976ff&#x27;, &#x27;#fed976ff&#x27;, &#x27;#fed976ff&#x27;, &#x27;#fed976ff&#x27;, &#x27;#fed976ff&#x27;, &#x27;#fed976ff&#x27;, &#x27;#fed976ff&#x27;, &#x27;#fed976ff&#x27;, &#x27;#fed976ff&#x27;, &#x27;#fed976ff&#x27;, &#x27;#fed976ff&#x27;, &#x27;#fed976ff&#x27;, &#x27;#fed976ff&#x27;, &#x27;#fed976ff&#x27;, &#x27;#fed976ff&#x27;, &#x27;#fed976ff&#x27;, &#x27;#fed976ff&#x27;, &#x27;#fed976ff&#x27;, &#x27;#fed976ff&#x27;, &#x27;#fed976ff&#x27;, &#x27;#fed976ff&#x27;, &#x27;#fed976ff&#x27;, &#x27;#fed976ff&#x27;, &#x27;#fed976ff&#x27;, &#x27;#fed976ff&#x27;, &#x27;#feb24cff&#x27;, &#x27;#feb24cff&#x27;, &#x27;#feb24cff&#x27;, &#x27;#feb24cff&#x27;, &#x27;#feb24cff&#x27;, &#x27;#feb24cff&#x27;, &#x27;#feb24cff&#x27;, &#x27;#feb24cff&#x27;, &#x27;#feb24cff&#x27;, &#x27;#feb24cff&#x27;, &#x27;#feb24cff&#x27;, &#x27;#feb24cff&#x27;, &#x27;#feb24cff&#x27;, &#x27;#feb24cff&#x27;, &#x27;#feb24cff&#x27;, &#x27;#feb24cff&#x27;, &#x27;#feb24cff&#x27;, &#x27;#feb24cff&#x27;, &#x27;#feb24cff&#x27;, &#x27;#feb24cff&#x27;, &#x27;#feb24cff&#x27;, &#x27;#feb24cff&#x27;, &#x27;#feb24cff&#x27;, &#x27;#feb24cff&#x27;, &#x27;#feb24cff&#x27;, &#x27;#feb24cff&#x27;, &#x27;#feb24cff&#x27;, &#x27;#feb24cff&#x27;, &#x27;#feb24cff&#x27;, &#x27;#feb24cff&#x27;, &#x27;#feb24cff&#x27;, &#x27;#feb24cff&#x27;, &#x27;#feb24cff&#x27;, &#x27;#feb24cff&#x27;, &#x27;#feb24cff&#x27;, &#x27;#feb24cff&#x27;, &#x27;#feb24cff&#x27;, &#x27;#feb24cff&#x27;, &#x27;#feb24cff&#x27;, &#x27;#feb24cff&#x27;, &#x27;#feb24cff&#x27;, &#x27;#feb24cff&#x27;, &#x27;#feb24cff&#x27;, &#x27;#feb24cff&#x27;, &#x27;#feb24cff&#x27;, &#x27;#feb24cff&#x27;, &#x27;#feb24cff&#x27;, &#x27;#feb24cff&#x27;, &#x27;#feb24cff&#x27;, &#x27;#feb24cff&#x27;, &#x27;#feb24cff&#x27;, &#x27;#feb24cff&#x27;, &#x27;#feb24cff&#x27;, &#x27;#feb24cff&#x27;, &#x27;#feb24cff&#x27;, &#x27;#feb24cff&#x27;, &#x27;#feb24cff&#x27;, &#x27;#feb24cff&#x27;, &#x27;#feb24cff&#x27;, &#x27;#feb24cff&#x27;, &#x27;#feb24cff&#x27;, &#x27;#feb24cff&#x27;, &#x27;#feb24cff&#x27;, &#x27;#feb24cff&#x27;, &#x27;#feb24cff&#x27;, &#x27;#feb24cff&#x27;, &#x27;#feb24cff&#x27;, &#x27;#feb24cff&#x27;, &#x27;#feb24cff&#x27;, &#x27;#feb24cff&#x27;, &#x27;#feb24cff&#x27;, &#x27;#feb24cff&#x27;, &#x27;#feb24cff&#x27;, &#x27;#feb24cff&#x27;, &#x27;#feb24cff&#x27;, &#x27;#feb24cff&#x27;, &#x27;#feb24cff&#x27;, &#x27;#feb24cff&#x27;, &#x27;#feb24cff&#x27;, &#x27;#feb24cff&#x27;, &#x27;#feb24cff&#x27;, &#x27;#feb24cff&#x27;, &#x27;#feb24cff&#x27;, &#x27;#fd8d3cff&#x27;, &#x27;#fd8d3cff&#x27;, &#x27;#fd8d3cff&#x27;, &#x27;#fd8d3cff&#x27;, &#x27;#fd8d3cff&#x27;, &#x27;#fd8d3cff&#x27;, &#x27;#fd8d3cff&#x27;, &#x27;#fd8d3cff&#x27;, &#x27;#fd8d3cff&#x27;, &#x27;#fd8d3cff&#x27;, &#x27;#fd8d3cff&#x27;, &#x27;#fd8d3cff&#x27;, &#x27;#fd8d3cff&#x27;, &#x27;#fd8d3cff&#x27;, &#x27;#fd8d3cff&#x27;, &#x27;#fd8d3cff&#x27;, &#x27;#fd8d3cff&#x27;, &#x27;#fd8d3cff&#x27;, &#x27;#fd8d3cff&#x27;, &#x27;#fd8d3cff&#x27;, &#x27;#fd8d3cff&#x27;, &#x27;#fd8d3cff&#x27;, &#x27;#fd8d3cff&#x27;, &#x27;#fd8d3cff&#x27;, &#x27;#fd8d3cff&#x27;, &#x27;#fd8d3cff&#x27;, &#x27;#fd8d3cff&#x27;, &#x27;#fd8d3cff&#x27;, &#x27;#fd8d3cff&#x27;, &#x27;#fd8d3cff&#x27;, &#x27;#fd8d3cff&#x27;, &#x27;#fd8d3cff&#x27;, &#x27;#fd8d3cff&#x27;, &#x27;#fd8d3cff&#x27;, &#x27;#fd8d3cff&#x27;, &#x27;#fd8d3cff&#x27;, &#x27;#fd8d3cff&#x27;, &#x27;#fd8d3cff&#x27;, &#x27;#fd8d3cff&#x27;, &#x27;#fd8d3cff&#x27;, &#x27;#fd8d3cff&#x27;, &#x27;#fd8d3cff&#x27;, &#x27;#fd8d3cff&#x27;, &#x27;#fd8d3cff&#x27;, &#x27;#fd8d3cff&#x27;, &#x27;#fd8d3cff&#x27;, &#x27;#fd8d3cff&#x27;, &#x27;#fd8d3cff&#x27;, &#x27;#fd8d3cff&#x27;, &#x27;#fd8d3cff&#x27;, &#x27;#fd8d3cff&#x27;, &#x27;#fd8d3cff&#x27;, &#x27;#fd8d3cff&#x27;, &#x27;#fd8d3cff&#x27;, &#x27;#fd8d3cff&#x27;, &#x27;#fd8d3cff&#x27;, &#x27;#fd8d3cff&#x27;, &#x27;#fd8d3cff&#x27;, &#x27;#fd8d3cff&#x27;, &#x27;#fd8d3cff&#x27;, &#x27;#fd8d3cff&#x27;, &#x27;#fd8d3cff&#x27;, &#x27;#fd8d3cff&#x27;, &#x27;#fd8d3cff&#x27;, &#x27;#fd8d3cff&#x27;, &#x27;#fd8d3cff&#x27;, &#x27;#fd8d3cff&#x27;, &#x27;#fd8d3cff&#x27;, &#x27;#fd8d3cff&#x27;, &#x27;#fd8d3cff&#x27;, &#x27;#fd8d3cff&#x27;, &#x27;#fd8d3cff&#x27;, &#x27;#fd8d3cff&#x27;, &#x27;#fd8d3cff&#x27;, &#x27;#fd8d3cff&#x27;, &#x27;#fd8d3cff&#x27;, &#x27;#fd8d3cff&#x27;, &#x27;#fd8d3cff&#x27;, &#x27;#fd8d3cff&#x27;, &#x27;#fd8d3cff&#x27;, &#x27;#fd8d3cff&#x27;, &#x27;#fd8d3cff&#x27;, &#x27;#fd8d3cff&#x27;, &#x27;#f03b20ff&#x27;, &#x27;#f03b20ff&#x27;, &#x27;#f03b20ff&#x27;, &#x27;#f03b20ff&#x27;, &#x27;#f03b20ff&#x27;, &#x27;#f03b20ff&#x27;, &#x27;#f03b20ff&#x27;, &#x27;#f03b20ff&#x27;, &#x27;#f03b20ff&#x27;, &#x27;#f03b20ff&#x27;, &#x27;#f03b20ff&#x27;, &#x27;#f03b20ff&#x27;, &#x27;#f03b20ff&#x27;, &#x27;#f03b20ff&#x27;, &#x27;#f03b20ff&#x27;, &#x27;#f03b20ff&#x27;, &#x27;#f03b20ff&#x27;, &#x27;#f03b20ff&#x27;, &#x27;#f03b20ff&#x27;, &#x27;#f03b20ff&#x27;, &#x27;#f03b20ff&#x27;, &#x27;#f03b20ff&#x27;, &#x27;#f03b20ff&#x27;, &#x27;#f03b20ff&#x27;, &#x27;#f03b20ff&#x27;, &#x27;#f03b20ff&#x27;, &#x27;#f03b20ff&#x27;, &#x27;#f03b20ff&#x27;, &#x27;#f03b20ff&#x27;, &#x27;#f03b20ff&#x27;, &#x27;#f03b20ff&#x27;, &#x27;#f03b20ff&#x27;, &#x27;#f03b20ff&#x27;, &#x27;#f03b20ff&#x27;, &#x27;#f03b20ff&#x27;, &#x27;#f03b20ff&#x27;, &#x27;#f03b20ff&#x27;, &#x27;#f03b20ff&#x27;, &#x27;#f03b20ff&#x27;, &#x27;#f03b20ff&#x27;, &#x27;#f03b20ff&#x27;, &#x27;#f03b20ff&#x27;, &#x27;#f03b20ff&#x27;, &#x27;#f03b20ff&#x27;, &#x27;#f03b20ff&#x27;, &#x27;#f03b20ff&#x27;, &#x27;#f03b20ff&#x27;, &#x27;#f03b20ff&#x27;, &#x27;#f03b20ff&#x27;, &#x27;#f03b20ff&#x27;, &#x27;#f03b20ff&#x27;, &#x27;#f03b20ff&#x27;, &#x27;#f03b20ff&#x27;, &#x27;#f03b20ff&#x27;, &#x27;#f03b20ff&#x27;, &#x27;#f03b20ff&#x27;, &#x27;#f03b20ff&#x27;, &#x27;#f03b20ff&#x27;, &#x27;#f03b20ff&#x27;, &#x27;#f03b20ff&#x27;, &#x27;#f03b20ff&#x27;, &#x27;#f03b20ff&#x27;, &#x27;#f03b20ff&#x27;, &#x27;#f03b20ff&#x27;, &#x27;#f03b20ff&#x27;, &#x27;#f03b20ff&#x27;, &#x27;#f03b20ff&#x27;, &#x27;#f03b20ff&#x27;, &#x27;#f03b20ff&#x27;, &#x27;#f03b20ff&#x27;, &#x27;#f03b20ff&#x27;, &#x27;#f03b20ff&#x27;, &#x27;#f03b20ff&#x27;, &#x27;#f03b20ff&#x27;, &#x27;#f03b20ff&#x27;, &#x27;#f03b20ff&#x27;, &#x27;#f03b20ff&#x27;, &#x27;#f03b20ff&#x27;, &#x27;#f03b20ff&#x27;, &#x27;#f03b20ff&#x27;, &#x27;#f03b20ff&#x27;, &#x27;#f03b20ff&#x27;, &#x27;#f03b20ff&#x27;, &#x27;#bd0026ff&#x27;, &#x27;#bd0026ff&#x27;, &#x27;#bd0026ff&#x27;, &#x27;#bd0026ff&#x27;, &#x27;#bd0026ff&#x27;, &#x27;#bd0026ff&#x27;, &#x27;#bd0026ff&#x27;, &#x27;#bd0026ff&#x27;, &#x27;#bd0026ff&#x27;, &#x27;#bd0026ff&#x27;, &#x27;#bd0026ff&#x27;, &#x27;#bd0026ff&#x27;, &#x27;#bd0026ff&#x27;, &#x27;#bd0026ff&#x27;, &#x27;#bd0026ff&#x27;, &#x27;#bd0026ff&#x27;, &#x27;#bd0026ff&#x27;, &#x27;#bd0026ff&#x27;, &#x27;#bd0026ff&#x27;, &#x27;#bd0026ff&#x27;, &#x27;#bd0026ff&#x27;, &#x27;#bd0026ff&#x27;, &#x27;#bd0026ff&#x27;, &#x27;#bd0026ff&#x27;, &#x27;#bd0026ff&#x27;, &#x27;#bd0026ff&#x27;, &#x27;#bd0026ff&#x27;, &#x27;#bd0026ff&#x27;, &#x27;#bd0026ff&#x27;, &#x27;#bd0026ff&#x27;, &#x27;#bd0026ff&#x27;, &#x27;#bd0026ff&#x27;, &#x27;#bd0026ff&#x27;, &#x27;#bd0026ff&#x27;, &#x27;#bd0026ff&#x27;, &#x27;#bd0026ff&#x27;, &#x27;#bd0026ff&#x27;, &#x27;#bd0026ff&#x27;, &#x27;#bd0026ff&#x27;, &#x27;#bd0026ff&#x27;, &#x27;#bd0026ff&#x27;, &#x27;#bd0026ff&#x27;, &#x27;#bd0026ff&#x27;, &#x27;#bd0026ff&#x27;, &#x27;#bd0026ff&#x27;, &#x27;#bd0026ff&#x27;, &#x27;#bd0026ff&#x27;, &#x27;#bd0026ff&#x27;, &#x27;#bd0026ff&#x27;, &#x27;#bd0026ff&#x27;, &#x27;#bd0026ff&#x27;, &#x27;#bd0026ff&#x27;, &#x27;#bd0026ff&#x27;, &#x27;#bd0026ff&#x27;, &#x27;#bd0026ff&#x27;, &#x27;#bd0026ff&#x27;, &#x27;#bd0026ff&#x27;, &#x27;#bd0026ff&#x27;, &#x27;#bd0026ff&#x27;, &#x27;#bd0026ff&#x27;, &#x27;#bd0026ff&#x27;, &#x27;#bd0026ff&#x27;, &#x27;#bd0026ff&#x27;, &#x27;#bd0026ff&#x27;, &#x27;#bd0026ff&#x27;, &#x27;#bd0026ff&#x27;, &#x27;#bd0026ff&#x27;, &#x27;#bd0026ff&#x27;, &#x27;#bd0026ff&#x27;, &#x27;#bd0026ff&#x27;, &#x27;#bd0026ff&#x27;, &#x27;#bd0026ff&#x27;, &#x27;#bd0026ff&#x27;, &#x27;#bd0026ff&#x27;, &#x27;#bd0026ff&#x27;, &#x27;#bd0026ff&#x27;, &#x27;#bd0026ff&#x27;, &#x27;#bd0026ff&#x27;, &#x27;#bd0026ff&#x27;, &#x27;#bd0026ff&#x27;, &#x27;#bd0026ff&#x27;, &#x27;#bd0026ff&#x27;, &#x27;#bd0026ff&#x27;, &#x27;#bd0026ff&#x27;]);


    color_map_46d3efdc768d9c81e7d1ed947571f2a2.x = d3.scale.linear()
              .domain([1.7, 7.2])
              .range([0, 450 - 50]);

    color_map_46d3efdc768d9c81e7d1ed947571f2a2.legend = L.control({position: &#x27;topright&#x27;});
    color_map_46d3efdc768d9c81e7d1ed947571f2a2.legend.onAdd = function (map) {var div = L.DomUtil.create(&#x27;div&#x27;, &#x27;legend&#x27;); return div};
    color_map_46d3efdc768d9c81e7d1ed947571f2a2.legend.addTo(map_9acbafbc0805ac35fc08414fa62c4426);

    color_map_46d3efdc768d9c81e7d1ed947571f2a2.xAxis = d3.svg.axis()
        .scale(color_map_46d3efdc768d9c81e7d1ed947571f2a2.x)
        .orient(&quot;top&quot;)
        .tickSize(1)
        .tickValues([1.7, 2.6166666666666667, 3.533333333333333, 4.45, 5.366666666666666, 6.283333333333333, 7.2]);

    color_map_46d3efdc768d9c81e7d1ed947571f2a2.svg = d3.select(&quot;.legend.leaflet-control&quot;).append(&quot;svg&quot;)
        .attr(&quot;id&quot;, &#x27;legend&#x27;)
        .attr(&quot;width&quot;, 450)
        .attr(&quot;height&quot;, 40);

    color_map_46d3efdc768d9c81e7d1ed947571f2a2.g = color_map_46d3efdc768d9c81e7d1ed947571f2a2.svg.append(&quot;g&quot;)
        .attr(&quot;class&quot;, &quot;key&quot;)
        .attr(&quot;transform&quot;, &quot;translate(25,16)&quot;);

    color_map_46d3efdc768d9c81e7d1ed947571f2a2.g.selectAll(&quot;rect&quot;)
        .data(color_map_46d3efdc768d9c81e7d1ed947571f2a2.color.range().map(function(d, i) {
          return {
            x0: i ? color_map_46d3efdc768d9c81e7d1ed947571f2a2.x(color_map_46d3efdc768d9c81e7d1ed947571f2a2.color.domain()[i - 1]) : color_map_46d3efdc768d9c81e7d1ed947571f2a2.x.range()[0],
            x1: i &lt; color_map_46d3efdc768d9c81e7d1ed947571f2a2.color.domain().length ? color_map_46d3efdc768d9c81e7d1ed947571f2a2.x(color_map_46d3efdc768d9c81e7d1ed947571f2a2.color.domain()[i]) : color_map_46d3efdc768d9c81e7d1ed947571f2a2.x.range()[1],
            z: d
          };
        }))
      .enter().append(&quot;rect&quot;)
        .attr(&quot;height&quot;, 40 - 30)
        .attr(&quot;x&quot;, function(d) { return d.x0; })
        .attr(&quot;width&quot;, function(d) { return d.x1 - d.x0; })
        .style(&quot;fill&quot;, function(d) { return d.z; });

    color_map_46d3efdc768d9c81e7d1ed947571f2a2.g.call(color_map_46d3efdc768d9c81e7d1ed947571f2a2.xAxis).append(&quot;text&quot;)
        .attr(&quot;class&quot;, &quot;caption&quot;)
        .attr(&quot;y&quot;, 21)
        .text(&quot;Unemployment rate %&quot;);

                choropleth_7166844dd7229e547513835f2a28ea67.addTo(map_9acbafbc0805ac35fc08414fa62c4426);
&lt;/script&gt;
&lt;/html&gt;" style="position:absolute;width:100%;height:100%;left:0;top:0;border:none !important;" allowfullscreen webkitallowfullscreen mozallowfullscreen></iframe></div></div>



If you hover over the LGA you can see the name of the council as well as the unemployment rate.

As you can see, Fairfield has the highest unemployment rate and Camden has the lowest unemployment rate.


```python
sydney_lgas_unemployment.sort_values('unemployment_rate').tail(1)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>LGA</th>
      <th>Data item</th>
      <th>unemployment_rate</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>12</th>
      <td>FAIRFIELD</td>
      <td>Smoothed unemployment rate (%)</td>
      <td>7.2</td>
    </tr>
  </tbody>
</table>
</div>




```python
sydney_lgas_unemployment.sort_values('unemployment_rate').head(1)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>LGA</th>
      <th>Data item</th>
      <th>unemployment_rate</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>9</th>
      <td>CAMDEN</td>
      <td>Smoothed unemployment rate (%)</td>
      <td>1.7</td>
    </tr>
  </tbody>
</table>
</div>

For the source code/Jupyter notebook please see this [Github repo](https://github.com/ben-n93/sydney_unemployment_rate).

