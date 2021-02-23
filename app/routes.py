from flask import render_template
from app import app
from app.data_reader import DataReader
from app.util import prettify_datarow


@app.route('/')
@app.route('/index')
def index():
    reader = DataReader()
    data = reader.get_data()
    for loc in data["locations"]:
        loc = prettify_datarow(loc)
    return render_template('index.html', data=data)