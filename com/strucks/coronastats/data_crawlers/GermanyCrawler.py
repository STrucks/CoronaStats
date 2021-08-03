import json
import os
import time
from abc import ABC

import requests

from com.strucks.coronastats.data_crawlers.AbstractDataCrawler import AbstractDataCrawler
from com.strucks.coronastats.data_manager import DataManager
from com.strucks.coronastats.models import OverviewDataRow


class GermanyCrawler(AbstractDataCrawler):

    def __init__(self):
        super().__init__("https://covid-19-data.p.rapidapi.com/country?name=germany")
        self.headers = {
            'x-rapidapi-key': os.environ.get("COVID19_APIKEY"),
            'x-rapidapi-host': "covid-19-data.p.rapidapi.com"
        }

    def get_location(self) -> str:
        return "Germany"

    def refresh(self) -> OverviewDataRow:
        response = requests.get(self.url, headers=self.headers)
        if response.status_code == 429:
            print("[%s] could not crawl the world wide data because of 429 error. Will wait a bit..." % time.ctime())
            time.sleep(2)
            entry = self.refresh()
            return entry
        if response.status_code == 401:
            raise Exception("Invalid API token")
        print(response.status_code)
        response = json.loads(response.text)[0]

        if response["confirmed"] is not None and response["deaths"] is not None and response["recovered"] is not None:
            active_cases = response["confirmed"] - response["deaths"] - response["recovered"]
        else:
            active_cases = "Not Available"

        entry = OverviewDataRow(location="germany", incidence=-1, active=active_cases,
                                deaths=response.get("deaths", -1), cured=response.get("recovered", -1),
                                cases=response.get("confirmed", -1), timestamp=time.time())
        self.latest = entry
        self.update(entry)
        print("successfully crawled %s data" % self.get_location())
        return entry
