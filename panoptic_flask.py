import json
import geopandas as gpd
from flask import Flask, render_template
from folium_map import generate_map
app = Flask(__name__)

with open('./shape_files/india_gdf.json') as response:
    india_gdf = json.load(response)

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


@app.route('/')
def root():
    html_map = generate_map(geojson=india_gdf, data=gdf)
    return render_template('home.html', iframe=html_map)


@app.route('/state/<state>')
def get_frts(state):
    return state


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
