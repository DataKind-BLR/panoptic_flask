import os
import json
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

print(model.get_home_page_data())
print('----------------------------')
import pdb
pdb.set_trace()


@app.route('/')
def root():
    shape_df['state_total'] = 7         # SAMPLE ALL STATES = 7
    html_map = generate_map(map_json, shape_df)
    return render_template('home.html', data={
        'iframe': html_map,
        'states': shape_df[['st_nm', 'state_total']].to_dict(orient='records')
    })


@app.route('/state/<state>')
def get_frts(state):
    state_data = {
        'name': state,
        'total_frts': 20,
        'total_in_use': 17,
        'total_not_in_use': 3,
        'financial_outlay_cr': 150,
        'frts': [{
            'name': 'Delhi Airport: Digiyatra',
            'in_use': True,
            'purpose': 'Authentication of Identity',
            'report_use_on': 'Sept 2018 onwards',
            'rti_filed_on': '3rd Dec 2018',
            'financial_outlay_cr': 3.4,
            'media_source': 'https://internetfreedom.in/',
            'rti_response': 'https://internetfreedom.in/'
        }, {
            'name': 'Soemthing Else',
            'in_use': False,
            'purpose': 'Authentication of Identity',
            'report_use_on': 'Sept 2018 onwards',
            'rti_filed_on': '3rd Dec 2018',
            'financial_outlay_cr': 3.4,
            'media_source': 'https://internetfreedom.in/',
            'rti_response': 'https://internetfreedom.in/'
        }, {
            'name': 'Another',
            'in_use': True,
            'purpose': 'Authentication of Identity',
            'report_use_on': 'Sept 2018 onwards',
            'rti_filed_on': '3rd Dec 2018',
            'financial_outlay_cr': 3.4,
            'media_source': 'https://internetfreedom.in/',
            'rti_response': 'https://internetfreedom.in/'
        }]
    }
    return render_template('state.html', state=state_data)


@app.route('/submit_frt')
def submit_frt():
    return render_template('submit_frt.html')


@app.route('/case_studies')
def case_studies():
    return render_template('case_studies.html')


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
