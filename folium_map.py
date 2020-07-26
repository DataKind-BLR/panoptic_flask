import geopandas as gpd
import pandas as pd
import folium
import branca
import requests
import json
from folium import IFrame
from folium.features import GeoJson, GeoJsonTooltip, GeoJsonPopup

def generate_map():
    gdf = gpd.read_file('./shape_files/states_india.shp')

    gdf['Count of FRT Systems'] = 0
    gdf['FRT Systems Deployed'] = 'None'
    gdf['Authority'] = 'None'
    gdf['Place'] = 'None'
    gdf['Purpose'] = 'None'

    gdf['FRT Systems Deployed'][0] = 'TSCOP + CCTNS'
    gdf['Count of FRT Systems'][0] = 1
    gdf['Authority'][0] = 'Hyderabad Police'
    gdf['Place'][0] = 'Hyderabad'
    gdf['Purpose'][0] = 'Security/ Surveillance'

    gdf['FRT Systems Deployed'][35] = 'AFRS'
    gdf['Count of FRT Systems'][35] = 1
    gdf['Authority'][35] = 'Delhi Police'
    gdf['Place'][35] = 'Delhi'
    gdf['Purpose'][35] = 'Security/ Surveillance'

    gdf['FRT Systems Deployed'][27] = 'Trinetra'
    gdf['Count of FRT Systems'][27] = 1
    gdf['Authority'][27] = 'UP Police'
    gdf['Place'][27] = 'UP/Lucknow'
    gdf['Purpose'][27] = 'Security/ Surveillance'

    gdf['FRT Systems Deployed'][25] = 'FaceTagr'
    gdf['Count of FRT Systems'][25] = 1
    gdf['Authority'][25] = 'Chennai Police'
    gdf['Place'][25] = 'Chennai'
    gdf['Purpose'][25] = 'Security/ Surveillance'

    gdf['FRT Systems Deployed'][22] = 'Punjab Artificial Intelligence System'
    gdf['Count of FRT Systems'][22] = 1
    gdf['Authority'][22] = 'Punjab Police'
    gdf['Place'][22] = 'Punjab'
    gdf['Purpose'][22] = 'Security/ Surveillance'

    gdf['FRT Systems Deployed'][14] = 'South Western Railways'
    gdf['Count of FRT Systems'][14] = 1
    gdf['Authority'][14] = 'South Western Railways'
    gdf['Place'][14] = 'KSR Bengaluru Station'
    gdf['Purpose'][14] = 'Security/ Surveillance'

    gdf.to_file("india_gdf.json", driver="GeoJSON")
    
    with open('./shape_files/india_gdf.json') as response:
        india_gdf = json.load(response)

    # Create a white image of 4 pixels, and embed it in a url.
    white_tile = branca.utilities.image_to_url([[1, 1], [1, 1]])

    f = folium.Figure() #width='container', height=700
    m = folium.Map([23.53, 78.3], maxZoom=5,minZoom=4.0,zoom_control=True,zoom_start=4,
                scrollWheelZoom=True,maxBounds=[[40, 68],[6, 97]],tiles=white_tile,attr='white tile',
                dragging=True,width = '100%',height = '100%').add_to(f)

    #folium.GeoJson(india).add_to(m)

    popup = GeoJsonPopup(
        fields=['st_nm','FRT Systems Deployed','Authority','Place','Purpose'],
        aliases=['State','FRT Systems Deployed','Authority','Place','Purpose'],
        localize=True,
        labels=True,
        style='''background-color: white;
                border-radius: 3px;''',
    )

    tooltip = GeoJsonTooltip(
        fields=['st_nm','cartodb_id'],
        aliases=['State',"FRT Systems Deployed"],
        localize=True,
        sticky=False,
        labels=True,
        style="""
            background-color: #F0EFEF;
            border: 1px solid black;
            border-radius: 3px;
            box-shadow: 3px;
        """,
        max_width=800,
    )

    g = folium.Choropleth(
        geo_data=india_gdf,
        data=gdf,
        columns=['st_nm','Count of FRT Systems'],
        key_on='properties.st_nm',
        fill_color='Set3',
        fill_opacity=0.7,
        line_opacity=0.4,
        legend_name='FRT Systems',
        highlight=True,
        
    ).add_to(m)
    for key in g._children:
        if key.startswith('color_map'):
            del(g._children[key])

    for i in range(len(india_gdf['features'])):
        gs = folium.GeoJson(india_gdf['features'][i],
                        style_function=lambda feature: {
                            'fillColor': '#ffff00',
                            'color': 'black',
                            'weight': 0.1,
                            'dashArray': '5, 5'
                        })
        state = india_gdf['features'][i]['properties']['st_nm']
        auth = india_gdf['features'][i]['properties']['Authority']
        html = f'''
        <h1>Name: </h1>{state}<br />\
        <h2>Location: </h2>{auth}<br />\
        <a href="about:blank">More Details</a>
        '''
        iframe = IFrame(html, width=250, height=200)
        folium.Popup(iframe, max_width=500).add_to(gs)
        gs.add_to(g)

    f.save('./templates/map_plot.html')
    #html_string = f.get_root().render()
    html_string = f.get_root().render()
    return html_string