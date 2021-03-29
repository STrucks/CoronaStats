import datetime
import json
import time

import yaml


class DataReader:
    """
    This class ready the latest crawled data from the data store.
    """

    def get_data(self):
        """
        Gets the stats data from the latest json file
        :param location:
        :return:
        """
        print("Reading Data")
        # load the latest file:
        with open("./data/stats_latest.json", "r", encoding="utf-8") as f:
            latest = json.load(f)
        with open("./app/conf.yaml", "r", encoding="utf-8") as f:
            conf = yaml.load(f, Loader=yaml.Loader)
        data = {"locations": [],
                "meta": {
                    "refresh": time.ctime()
                }}
        latest_timestamp = 0
        for loc in conf["available_location_keys"].keys():
            try:
                data_entry = self.get_by_location(latest, loc, conf["available_location_keys"][loc])
                if data_entry["time"] > latest_timestamp:
                    latest_timestamp = data_entry["time"]
                data["locations"].append(data_entry)
            except Exception as e:
                print(str(e))
                data["locations"].append({
                        "name": loc,
                        "incidence": "Not Available",
                        "active_cases": "Not Available",
                        "died": "Not Available",
                        "cured": "Not Available",
                        "cases": "Not Available"
                    })
        data["meta"]["timestamp"] = datetime.datetime.fromtimestamp(latest_timestamp).strftime("%m/%d/%Y, %H:%M:%S")
        return data

    def get_by_location(self, data, loc_name, loc_key):
        data_row = data.get(loc_key)
        return {
            "name": loc_name,
            "incidence": data_row["incidence"],  # float
            "active_cases": data_row["active"],
            "died": data_row["deaths"],
            "cured": data_row["cured"],
            "cases": data_row["total"],
            "time": float(data_row["timestamp"])
        }

    def get_world_wide(self, data):
        data_row = data.get("world_wide")
        return {
            "name": "Weltweit",
            "incidence": data_row["incidence"],  # float
            "active_cases": data_row["active"],
            "died": data_row["deaths"],
            "cured": data_row["cured"],
            "cases": data_row["total"]
        }

    def get_germany(self, data):
        data_row = data.get("germany")
        return {
            "name": "Deutschland",
            "incidence": data_row["incidence"],  # float
            "active_cases": data_row["active"],
            "died": data_row["deaths"],
            "cured": data_row["cured"],
            "cases": data_row["total"]
        }

    def get_kleve(self, data):
        data_row = data.get("kleve")
        return {
            "name": "Kreis Kleve",
            "incidence": data_row["incidence"],  # float
            "active_cases": data_row["active"],
            "died": data_row["deaths"],
            "cured": data_row["cured"],
            "cases": data_row["total"]
        }

    def get_oberhausen(self, data):
        data_row = data.get("oberhausen")
        return {
            "name": "Oberhausen",
            "incidence": data_row["incidence"],  # float
            "active_cases": data_row["active"],
            "died": data_row["deaths"],
            "cured": data_row["cured"],
            "cases": data_row["total"]
        }

    def get_hannover(self, data):
        data_row = data.get("hannover")
        return {
            "name": "Hannover",
            "incidence": data_row["incidence"],  # float
            "active_cases": data_row["active"],
            "died": data_row["deaths"],
            "cured": data_row["cured"],
            "cases": data_row["total"]
        }
