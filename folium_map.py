import folium
import branca

def generate_map(map_json, data):
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
        fields=['st_nm'],
        aliases=['State'],
        localize=True,
        labels=True,
        style='''
            background-color: white;
            border-radius: 3px;
        ''',
    )

    g = folium.Choropleth(
        geo_data=map_json,
        data=data,
        columns=['st_nm', 'state_total'],           # from dataframe `data`
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

    for i in range(len(map_json['features'])):
        gs = folium.GeoJson(
            map_json['features'][i],
            style_function=lambda feature: {
                'fillColor': '#ffff00',
                'color': 'black',
                'weight': 0.1,
                'dashArray': '5, 5'
            }
        )

        state = map_json['features'][i]['properties']['st_nm']
        popup_html = '''
            <h1>{}</h1><br />\
            <h2>Total FRTs: </h2><br />\
            <a target="_blank" href="/state/{}">More Details</a>
        '''.format(state, state)
        
        popup = folium.IFrame(popup_html, width=200, height=150)
        folium.Popup(popup, max_width=300).add_to(gs)
        gs.add_to(g)

    return m._repr_html_()
