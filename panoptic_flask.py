import json
import geopandas as gpd
from folium_map import generate_map
from flask import Flask, render_template

app = Flask(__name__)

with open('./shape_files/india_gdf.json') as response:
    india_gdf = json.load(response)

shape_df = gpd.read_file('./shape_files/states_india.shp')


def merge_data(df):

    df['Count of FRT Systems'] = 0
    df['FRT Systems Deployed'] = 'None'
    df['Authority'] = 'None'
    df['Place'] = 'None'
    df['Purpose'] = 'None'

    df['FRT Systems Deployed'][0] = 'TSCOP + CCTNS'
    df['Count of FRT Systems'][0] = 1
    df['Authority'][0] = 'Hyderabad Police'
    df['Place'][0] = 'Hyderabad'
    df['Purpose'][0] = 'Security/ Surveillance'

    df['FRT Systems Deployed'][35] = 'AFRS'
    df['Count of FRT Systems'][35] = 1
    df['Authority'][35] = 'Delhi Police'
    df['Place'][35] = 'Delhi'
    df['Purpose'][35] = 'Security/ Surveillance'

    df['FRT Systems Deployed'][27] = 'Trinetra'
    df['Count of FRT Systems'][27] = 1
    df['Authority'][27] = 'UP Police'
    df['Place'][27] = 'UP/Lucknow'
    df['Purpose'][27] = 'Security/ Surveillance'

    df['FRT Systems Deployed'][25] = 'FaceTagr'
    df['Count of FRT Systems'][25] = 1
    df['Authority'][25] = 'Chennai Police'
    df['Place'][25] = 'Chennai'
    df['Purpose'][25] = 'Security/ Surveillance'

    df['FRT Systems Deployed'][22] = 'Punjab Artificial Intelligence System'
    df['Count of FRT Systems'][22] = 1
    df['Authority'][22] = 'Punjab Police'
    df['Place'][22] = 'Punjab'
    df['Purpose'][22] = 'Security/ Surveillance'

    df['FRT Systems Deployed'][14] = 'South Western Railways'
    df['Count of FRT Systems'][14] = 1
    df['Authority'][14] = 'South Western Railways'
    df['Place'][14] = 'KSR Bengaluru Station'
    df['Purpose'][14] = 'Security/ Surveillance'

    return df


'''
GLOBAL_DATA_HOME = {
    'total_frts': 54,
    'total_frts_national': 16,
    'total_frts_states': 38,
    'total_frts_submitted': 34, # count of FRTs submitted in survey (optional)
    'states': [{
          'state': 'Telangana',
          'state_total': 2
        }, {
          'state': 'Andaman & Nicobar Island',
          'state_total': 0
        },
        ...
    ]
}
'''

@app.route('/')
def root():
    formatted_df = merge_data(shape_df)
    html_map = generate_map(geojson=india_gdf, data=formatted_df)
    return render_template('home.html', iframe=html_map)


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


def total_frts(state='India'):
    if state == 'India':
        return main_df.count()
    return main_df.groupby(state).count()


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
    app.run()
