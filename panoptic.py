from flask import Flask, render_template

from folium_map import generate_map

app = Flask(__name__)


@app.route('/')
def root():
    generate_map()

    return render_template('home.html',iframe_map = generate_map())


@app.route('/map')
def map():
    return render_template('map_plot.html')


@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(
        debug=False,
        host='127.0.0.1',
        port=5000
    )
