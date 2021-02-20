import time

from flask import render_template
from app import app
from app.data_reader import DataReader
from backend.corona_api_client import CoronaGlobalClient, CoronaLocalClient
from util import prettify_datarow


@app.route('/')
@app.route('/index')
def index():
    client = CoronaGlobalClient()
    client_local = CoronaLocalClient()
    reader = DataReader()
    data = reader.get_data()
    for loc in data["locations"]:
        loc = prettify_datarow(loc)
    return render_template('index.html', data=data)