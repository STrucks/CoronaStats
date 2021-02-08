import json
import os
import time

import requests

from util import prettify_number


class CoronaGlobalClient:

    def __init__(self):
        self.headers = {

            'x-rapidapi-key': os.environ.get("COVID19_APIKEY"),
            'x-rapidapi-host': "covid-19-data.p.rapidapi.com"
        }

    def get_world_wide(self):
        time.sleep(1)
        url_world_wide = "https://covid-19-data.p.rapidapi.com/totals"
        response = requests.request("GET", url_world_wide, headers=self.headers)
        response = json.loads(response.text)[0]

        if response["confirmed"] is not None and response["deaths"] is not None and response["recovered"] is not None:
            active_cases = response["confirmed"] - response["deaths"] - response["recovered"]
        else:
            active_cases = "Not Available"

        return {
            "name": "Weltweit",
            "incidence": "Not Available",  # float
            "active_cases": active_cases,
            "cases": response.get("confirmed", "Not Available"),
            "died": response.get("deaths", "Not Available"),  # int
            "cured": response.get("recovered", "Not Available")  # int
        }

    def get_germany(self):
        time.sleep(1)
        url_germany = "https://covid-19-data.p.rapidapi.com/country"
        querystring = {"name": "germany"}
        response = requests.request("GET", url_germany, headers=self.headers, params=querystring)
        response = json.loads(response.text)[0]

        if response["confirmed"] is not None and response["deaths"] is not None and response["recovered"] is not None:
            active_cases = response["confirmed"] - response["deaths"] - response["recovered"]
        else:
            active_cases = "Not Available"

        return {
            "name": "Deutschland",
            "incidence": "Not Available",  # float
            "active_cases": active_cases,
            "cases": response.get("confirmed", "Not Available"),
            "died": response.get("deaths", "Not Available"),  # int
            "cured": response.get("recovered", "Not Available")  # int
        }


class CoronaLocalClient:

    def __init__(self):
        self.refresh()

    def get_oberhausen(self):
        return self.data["Oberhausen"]

    def get_hannover(self):
        return self.data["Hannover"]

    def get_kleve(self):
        return self.data["Kreis Kleve"]

    def refresh(self):
        self.data = {}
        url = "https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/services/RKI_Landkreisdaten/FeatureServer/0/query?objectIds=70,74,27&outFields=OBJECTID,cases7_per_100k,last_update,cases,deaths,recovered&returnGeometry=false&outSR=4326&f=json"
        response = requests.request("GET", url)
        response = json.loads(response.text)
        for region in response["features"]:
            attributes = region["attributes"]
            print(attributes)
            if attributes["OBJECTID"] == 27: # this is hannover
                name = "Hannover"
            elif attributes["OBJECTID"] == 70: # this is oberhausen
                name = "Oberhausen"
            elif attributes["OBJECTID"] == 74:  # this is Kleve
                name = "Kreis Kleve"
            else:
                raise Exception("Invalid Object Id %s" % attributes["OBJECT_ID"])

            if attributes["cases"] is not None and attributes["deaths"] is not None and attributes["recovered"] is not None:
                active_cases = attributes["cases"] - attributes["deaths"] - attributes["recovered"]
            else:
                active_cases = "Not Available"

            self.data[name] = {
                "name": name,
                "cases": attributes.get("cases", "Not Available"),
                "incidence": attributes.get("cases7_per_100k", "Not Available"),  # float
                "active_cases": active_cases,  # int
                "died": attributes.get("deaths", "Not Available"),  # int
                "cured": prettify_number(response.get("recovered", "Not Available"))  # int
            }


