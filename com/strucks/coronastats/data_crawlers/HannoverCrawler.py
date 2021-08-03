import json
import os
import time
from abc import ABC

import requests

from com.strucks.coronastats.data_crawlers.AbstractDataCrawler import AbstractDataCrawler
from com.strucks.coronastats.data_manager import DataManager
from com.strucks.coronastats.models import OverviewDataRow


class HannoverCrawler(AbstractDataCrawler):

    def __init__(self):
        super().__init__("https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/services/RKI_Landkreisdaten/FeatureServer/0/query?objectIds=27&outFields=OBJECTID,cases7_per_100k,last_update,cases,deaths,recovered&returnGeometry=false&outSR=4326&f=json")

    def get_location(self) -> str:
        return "Hannover"

    def refresh(self) -> OverviewDataRow:
        response = requests.get(self.url)
        response = json.loads(response.text)

        region = response["features"][0]
        attributes = region["attributes"]
        if attributes["cases"] is not None and attributes["deaths"] is not None and attributes["recovered"] is not None:
            active_cases = attributes["cases"] - attributes["deaths"] - attributes["recovered"]
        else:
            active_cases = -1

        entry = OverviewDataRow(location="hannover", incidence=attributes.get("cases7_per_100k", -1),
                                active=active_cases, deaths=response.get("deaths", -1),
                                cured=response.get("recovered", -1), cases=attributes.get("cases", -1),
                                timestamp=time.time())

        self.latest = entry
        self.update(entry)
        print("successfully crawled %s data" % self.get_location())
        return entry
