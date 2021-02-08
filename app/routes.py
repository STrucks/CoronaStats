import time

from flask import render_template
from app import app
from corona_api_client import CoronaGlobalClient, CoronaLocalClient
from util import prettify_datarow


@app.route('/')
@app.route('/index')
def index():
    client = CoronaGlobalClient()
    client_local = CoronaLocalClient()
    data = {
        "locations": [
            client.get_world_wide(),
            client.get_germany(),
            client_local.get_kleve(),
            client_local.get_oberhausen(),
            client_local.get_hannover()
        ],
        "meta": {
            "refresh": time.ctime()
        }
    }
    for loc in data["locations"]:
        loc = prettify_datarow(loc)
    return render_template('index.html', data=data)