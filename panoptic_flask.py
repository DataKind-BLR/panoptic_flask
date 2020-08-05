from flask import Flask, render_template
from folium_map import generate_map
app = Flask(__name__)


@app.route('/')
def root():
    # TODO: Srihari to generate iframe for map
    html_map = generate_map()
    return render_template('home.html', iframe=html_map)

@app.route('/map')
def map():
    return render_template('map_plot.html')

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
