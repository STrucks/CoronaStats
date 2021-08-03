import json
import os
import re
import time
from abc import ABC

import requests

from com.strucks.coronastats.data_crawlers.AbstractDataCrawler import AbstractDataCrawler
from com.strucks.coronastats.data_manager import DataManager
from com.strucks.coronastats.models import OverviewDataRow


class KranenburgCrawler(AbstractDataCrawler):

    def __init__(self):
        super().__init__("https://www.kreis-kleve.de/de/fachbereich5/corona-virus-daten-und-fakten-pressemitteilungen/")

    def get_location(self) -> str:
        return "Kranenburg"

    def refresh(self) -> OverviewDataRow:
        response = requests.request("GET", self.url)
        match = re.search(r"(?<=,\s)\d*(?=\sin\sKranenburg)", response.text)
        matched_text = response.text[match.start():match.end()]
        entry = OverviewDataRow(location="kranenburg", incidence=-1, active=-1, deaths=-1, cured=-1,
                                cases=int(matched_text), timestamp=time.time())
        self.latest = entry
        self.update(entry)
        print("successfully crawled %s data" % self.get_location())
        return entry
