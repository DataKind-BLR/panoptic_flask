import os
import json
import pandas as pd
import geopandas as gpd
from folium_map import generate_map
from flask import Flask, render_template
from model import model

app = Flask(__name__)
CURR_DIR = os.path.abspath(os.path.dirname(__file__))
MAP_JSON = os.path.join(CURR_DIR, 'shape_files/india_gdf.json')
STATES_INDIA = os.path.join(CURR_DIR, 'shape_files/states_india.shp')

with open(MAP_JSON) as response:
    map_json = json.load(response)

shape_df = gpd.read_file(STATES_INDIA)


@app.route('/')
def root():
    home_data = model.get_home_page_data()
    states_df = pd.DataFrame(home_data['states'])
    merged_df = shape_df.merge(states_df, left_on='st_nm', right_on='state')
    html_map = generate_map(map_json, merged_df)
    return render_template('home.html', data={
        'iframe': html_map,
        'totals': home_data
    })


@app.route('/state/<state>')
def get_frts(state):
    state_data = model.get_state_page_data(state)
    return render_template('state.html', state=state_data)


@app.route('/about')
def about():
    return render_template('about.html')


@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500


@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
