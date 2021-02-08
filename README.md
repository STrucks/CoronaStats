# Corona Stats
A small project to monitor the Corona infection numbers in (for me) relevant locations.
The goal of this project is to learn and experiment with a Flask based website and usage
of external APIs.

## Requirements
### API Keys
You need acces to the ``covid-19-data.p.rapidapi.com`` API for the Corona numbers worldwide and 
in Germany.
You have to get an API key for this API. To get one, visit ``https://rapidapi.com/Gramzivi/api/covid-19-data`` and 
register for the free subscription. Use the API key as a environment variable:

+ **COVID19_APIKEY**: "your-api-key"

### Run on local machine
Install requirements:

``pip install -r requirements.txt``

Set the ``FLASK_APP`` environment variable

Windows:
``
export FLASK_APP=frontend.py
``

Linux: 
``
set FLASK_APP=frontend.py
``

Finally, start the Flask server via

```
flask run
```

and open ``localhost:5000`` in your browser.