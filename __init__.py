import flask
import helper_functions
from flask import request, jsonify

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return "You are at home!"

@app.route('/single_frt', methods=['GET'])
def single_frt():

    # Check if state was provided as part of the URL.
    if 'state' in request.args:
        state = request.args['state']
    else:
        state = 'India'

    # Create an empty list for our results
    results = []

    headers, data = helper_functions.get_frt(state=state)

    while data:
        results.append(dict(zip(headers, data.pop())))

    return jsonify(results)

@app.route('/total_frts', methods=['GET'])
def total_frt():

    # Check if state was provided as part of the URL.
    if 'state' in request.args:
        state = request.args['state']
    else:
        state = 'India'

    headers, data = helper_functions.get_total_frt(state=state)

    while data:
        results = dict(zip(headers, data.pop()))

    return jsonify(results)

app.run()