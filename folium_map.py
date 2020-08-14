import folium
import branca

def generate_map(geojson, data):
    # Create a white image of 4 pixels, and embed it in a url.
    white_tile = branca.utilities.image_to_url([[1, 1], [1, 1]])

    m = folium.Map(
        [23.53, 78.3],
        maxZoom=7,
        minZoom=4,
        zoom_control=True,
        zoom_start=5,
        scrollWheelZoom=True,
        maxBounds=[[40, 68],[6, 97]],
        tiles=white_tile,
        attr='white tile',
        dragging=True
    )

    popup = folium.GeoJsonPopup(
        fields=['st_nm', 'FRT Systems Deployed', 'Authority', 'Place', 'Purpose'],
        aliases=['State', 'FRT Systems Deployed', 'Authority', 'Place', 'Purpose'],
        localize=True,
        labels=True,
        style='''
            background-color: white;
            border-radius: 3px;
        ''',
    )

    g = folium.Choropleth(
        geo_data=geojson,
        data=data,
        columns=['st_nm', 'Count of FRT Systems'],
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

    for i in range(len(geojson['features'])):
        gs = folium.GeoJson(
            geojson['features'][i],
            style_function=lambda feature: {
                'fillColor': '#ffff00',
                'color': 'black',
                'weight': 0.1,
                'dashArray': '5, 5'
            }
        )

        state = geojson['features'][i]['properties']['st_nm']
        auth = geojson['features'][i]['properties']['Authority']
        popup_html = '''
            <h1>Name: </h1>{}<br />\
            <h2>Location: </h2>{}<br />\
            <a target="_blank" href="/state/{}">More Details</a>
        '''.format(state, auth, state)
        
        popup = folium.IFrame(popup_html, width=200, height=150)
        folium.Popup(popup, max_width=300).add_to(gs)
        gs.add_to(g)

    return m._repr_html_()
