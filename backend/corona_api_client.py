import json
import os
import re
import time

import requests

from models.data_entry import DataEntry


class CoronaGlobalClient:

    def __init__(self):
        self.headers = {
            'x-rapidapi-key': os.environ.get("COVID19_APIKEY"),
            'x-rapidapi-host': "covid-19-data.p.rapidapi.com"
        }

    def get_data(self, location):
        """
        mapping for location name to data
        :param location:
        :return:
        """
        if location == "world_wide":
            return self.get_world_wide()
        elif location == "germany":
            return self.get_germany()
        else:
            raise Exception("Location %s not implemented" % location)

    def get_world_wide(self):
        time.sleep(1)
        url_world_wide = "https://covid-19-data.p.rapidapi.com/totals"
        response = requests.request("GET", url_world_wide, headers=self.headers)
        if response.status_code == 429:
            print("[%s] could not crawl the world wide data because of 429 error. Will wait a bit..." % time.ctime())
            time.sleep(2)
            entry = self.get_world_wide()
            return entry
        if response.status_code == 401:
            raise Exception("Invalid API token (%s)" % self.headers["x-rapidapi-key"])
        print(response.status_code)
        response = json.loads(response.text)[0]

        if response["confirmed"] is not None and response["deaths"] is not None and response["recovered"] is not None:
            active_cases = response["confirmed"] - response["deaths"] - response["recovered"]
        else:
            active_cases = "Not Available"
        incidence = _get_incidence("world_wide", response.get("confirmed", -1))
        entry = DataEntry(location="world_wide", incidence=incidence, active=active_cases, deaths=response.get("deaths", -1),
                          cured=response.get("recovered", -1), total=response.get("confirmed", -1),
                          timestamp=str(time.time()))
        return entry

    def get_germany(self):
        time.sleep(1)
        url_germany = "https://covid-19-data.p.rapidapi.com/country"
        querystring = {"name": "germany"}
        response = requests.request("GET", url_germany, headers=self.headers, params=querystring)
        if response.status_code == 429:
            print("[%s] could not crawl the world wide data because of 429 error. Will wait a bit..." % time.ctime())
            time.sleep(2)
            entry = self.get_world_wide()
            return entry
        if response.status_code == 401:
            raise Exception("Invalid API token")
        print(response.status_code)
        response = json.loads(response.text)[0]

        if response["confirmed"] is not None and response["deaths"] is not None and response["recovered"] is not None:
            active_cases = response["confirmed"] - response["deaths"] - response["recovered"]
        else:
            active_cases = "Not Available"
        incidence = _get_incidence("germany", response.get("confirmed", -1))
        entry = DataEntry(location="germany", incidence=incidence, active=active_cases, deaths=response.get("deaths", -1),
                          cured=response.get("recovered", -1), total=response.get("confirmed", -1),
                          timestamp=str(time.time()))
        return entry


class CoronaLocalClient:

    def __init__(self):
        self.refresh()

    def get_data(self, location):
        """
        mapping for location name to data
        :param location:
        :return:
        """
        if location == "oberhausen":
            return self.get_oberhausen()
        elif location == "hannover":
            return self.get_hannover()
        elif location == "kleve":
            return self.get_kleve()
        elif location == "kranenburg":
            return self.get_kranenburg()
        else:
            raise Exception("Location %s not implemented" % location)

    def get_oberhausen(self):
        return self.data["oberhausen"]

    def get_hannover(self):
        return self.data["hannover"]

    def get_kleve(self):
        return self.data["kleve"]

    def get_kranenburg(self):
        return self.data["kranenburg"]

    def refresh(self):
        self.data = {}
        # -- Oberhausen, Kleve and Hannover:
        url = "https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/services/RKI_Landkreisdaten/FeatureServer/0/query?objectIds=70,74,27&outFields=OBJECTID,cases7_per_100k,last_update,cases,deaths,recovered&returnGeometry=false&outSR=4326&f=json"
        response = requests.request("GET", url)
        response = json.loads(response.text)
        for region in response["features"]:
            attributes = region["attributes"]
            if attributes["OBJECTID"] == 27:  # this is hannover
                name = "hannover"
            elif attributes["OBJECTID"] == 70:  # this is oberhausen
                name = "oberhausen"
            elif attributes["OBJECTID"] == 74:  # this is Kleve
                name = "kleve"
            else:
                raise Exception("Invalid Object Id %s" % attributes["OBJECT_ID"])

            if attributes["cases"] is not None and attributes["deaths"] is not None and attributes[
                "recovered"] is not None:
                active_cases = attributes["cases"] - attributes["deaths"] - attributes["recovered"]
            else:
                active_cases = "Not Available"
            if attributes.get("cases7_per_100k", -1) == -1:
                attributes["cases7_per_100k"] = _get_incidence(name, attributes.get("cases", -1))
            entry = DataEntry(location=name, incidence=attributes.get("cases7_per_100k", -1), active=active_cases,
                              deaths=response.get("deaths", -1),
                              cured=response.get("recovered", -1), total=attributes.get("cases", -1),
                              timestamp=str(time.time()))

            self.data[name] = entry

        # Kranenburg:
        url = "https://www.kreis-kleve.de/de/fachbereich5/corona-virus-daten-und-fakten-pressemitteilungen/"
        response = requests.request("GET", url)
        try:
            match = re.search(r"(?<=,\s)\d*(?=\sin\sKranenburg)", response.text)
            matched_text = response.text[match.start():match.end()]
        except Exception as e:
            print(str(e))
        else:
            incidence = _get_incidence("kranenburg", int(matched_text))
            self.data["kranenburg"] = DataEntry(location="kranenburg", incidence=incidence, active=-1, deaths=-1, cured=-1,
                                            total=int(matched_text), timestamp=str(time.time()))

def _get_incidence(location_key, total_cases):
    try:
        # load the history data:
        with open("./data/stats_history.json", "r", encoding="utf-8") as f:
            history = json.load(f)
        # load the population data:
        with open("./data/population.json", "r", encoding="utf-8") as f:
            population = json.load(f)

        now = time.time()
        target_time = now - 7*24*60*60
        smallest_diff = min([(float(entry["timestamp"])-target_time)**2 for entry in history[location_key]])
        for entry in history[location_key]:
            if (float(entry["timestamp"])-target_time)**2 == smallest_diff:
                return (total_cases - entry["total"]) * (100000/population[location_key])

        return -1
    except Exception as e:
        print(str(e))
        return -1