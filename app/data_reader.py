import json
import time


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
        # load the latest file:
        with open("./data/stats_latest.json", "r", encoding="utf-8") as f:
            latest = json.load(f)
        try:
            data = {
                "locations": [
                    self.get_world_wide(latest),
                    self.get_germany(latest),
                    self.get_kleve(latest),
                    self.get_oberhausen(latest),
                    self.get_hannover(latest)
                ],
                "meta": {
                    "refresh": time.ctime()
                }
            }
        except Exception as e:
            print(str(e))
            data = {
                "locations": [
                    {
                        "name": "Weltweit",
                        "incidence": "Not Available",
                        "active_cases": "Not Available",
                        "died": "Not Available",
                        "cured": "Not Available",
                        "cases": "Not Available"
                    },
                    {
                        "name": "Deutschland",
                        "incidence": "Not Available",
                        "active_cases": "Not Available",
                        "died": "Not Available",
                        "cured": "Not Available",
                        "cases": "Not Available"
                    },
                    {
                        "name": "Kreis Kleve",
                        "incidence": "Not Available",
                        "active_cases": "Not Available",
                        "died": "Not Available",
                        "cured": "Not Available",
                        "cases": "Not Available"
                    },
                    {
                        "name": "Oberhausen",
                        "incidence": "Not Available",
                        "active_cases": "Not Available",
                        "died": "Not Available",
                        "cured": "Not Available",
                        "cases": "Not Available"
                    },
                    {
                        "name": "Hannover",
                        "incidence": "Not Available",
                        "active_cases": "Not Available",
                        "died": "Not Available",
                        "cured": "Not Available",
                        "cases": "Not Available"
                    },
                ],
                "meta": {
                    "refresh": time.ctime()
                }
            }
        finally:
            return data

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