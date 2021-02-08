import json

import requests

url = "https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/services/RKI_Landkreisdaten/FeatureServer/0/query?objectIds=70,74,27&outFields=OBJECTID,cases7_per_100k,last_update,cases,deaths,recovered&returnGeometry=false&outSR=4326&f=json"
response = requests.request("GET", url)
response = json.loads(response.text)
print()