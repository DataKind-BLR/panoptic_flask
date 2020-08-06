import json
import geopandas as gpd
import pandas as pd
from flask import Flask, render_template
from folium_map import generate_map
import sqlalchemy as sqla

app = Flask(__name__)

with open('./shape_files/india_gdf.json') as response:
    india_gdf = json.load(response)

gdf = gpd.read_file('./shape_files/states_india.shp')

# Step 1 - connect to DB
# sql_engine = sqla.create_engine('mysql+pymysql://root:ubuntu@ec2-3-7-235-141.ap-south-1.compute.amazonaws.com/panoptic')
# sql_connection = sql_engine.connect()

# Step 2 - get results in to a dataframe & cache it
# main_df = pd.read_sql('SELECT * FROM frt', sql_connection)
# last_updated = record time

# Step 3 - use the dataframe to return values

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


@app.route('/')
def root():
    html_map = generate_map(geojson=india_gdf, data=gdf)
    return render_template('home.html', iframe=html_map)

# last_updated = '5th August'

# def is_db_updated():
#     engine.connect()
#     db_date = pd.read_sql('SELECT timestamp from information_schema', connection)
#     if db_date > last_updated:
#         last_updated = db_date
#         return True
#     else:
#         return False 

@app.route('/state/<state>')
def get_frts(state):
    return state
    # if is_db_updated():
    #     main_df = pd.read_sql('SELECT * from frt', connection)
    # else:
    #     state_df = main_df[main_df['State'] == state]
    #     if state_df.empty:
    #         @app.errorhandler(500)
    #     return render_template('state.html', data=state_df.to_dict(orient='records'))


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
