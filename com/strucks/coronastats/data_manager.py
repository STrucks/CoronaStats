import json
import time

from com.strucks.coronastats.models import OverviewDataRow
from com.strucks.coronastats.util import Singleton


def crawler_life_cycle():
    from com.strucks.coronastats.data_crawlers.GermanyCrawler import GermanyCrawler
    from com.strucks.coronastats.data_crawlers.WorldWideCrawler import WorldWideCrawler
    from com.strucks.coronastats.data_crawlers.OberhausenCrawler import OberhausenCrawler
    from com.strucks.coronastats.data_crawlers.HannoverCrawler import HannoverCrawler
    from com.strucks.coronastats.data_crawlers.KleveCrawler import KleveCrawler
    from com.strucks.coronastats.data_crawlers.KranenburgCrawler import KranenburgCrawler
    # create the crawlers and store them in a list:
    crawlers = [
        WorldWideCrawler(),
        GermanyCrawler(),
        OberhausenCrawler(),
        KleveCrawler(),
        HannoverCrawler(),
        KranenburgCrawler(),
    ]

    # enter the life cycle
    while True:
        for crawler in crawlers:
            crawler.refresh()
        time.sleep(60)  # TODO get the time from config


@Singleton
class DataManager:

    def __init__(self):
        try:
            with open("./data/latest.json", "r", encoding="utf-8") as f:
                self.latest = json.load(f)
        except Exception:
            self.latest = json.loads(
                """{"world_wide":{},"germany":{},"oberhausen":{},"kleve":{},"hannover":{},"nimwegen":{}}""")
            with open("./data/latest.json", "w", encoding="utf-8") as f:
                json.dump(self.latest, f)
        try:
            with open("./data/history.json", "r", encoding="utf-8") as f:
                self.history = json.load(f)
        except Exception:
            self.history = json.loads("""{"world_wide":[],"germany":[],"oberhausen":[],"kleve":[],"hannover":[],"nimwegen":[]}""")
            with open("./data/latest.json", "w", encoding="utf-8") as f:
                json.dump(self.history, f)

        self.location_key_mapping = {
            "Germany": "germany",
            "Worldwide": "world_wide",
            "Oberhausen": "oberhausen",
            "Hannover": "hannover",
            "Kleve": "kleve",
            "Kranenburg": "kranenburg",
            "Nimwegen": "nimwegen",
        }
        self.api_key_mapping = {
            "world": "world_wide",
            "germany": "germany",
            "oberhausen": "oberhausen",
            "hannover": "hannover",
            "kleve": "kleve",
            "kranenburg": "kranenburg",
            "nijmegen": "nimwegen"
        }

    def update(self, location, entry: OverviewDataRow):
        location_key = self.location_key_mapping[location]
        if location_key not in self.latest.keys():
            self.latest[location_key] = {}
            self.history[location_key] = []
        if entry.cases != self.latest[location_key].get("cases", 0):
            self.latest[location_key] = entry.to_dict()
            self.history[location_key].append(entry.to_dict())
            with open("./data/latest.json", "w", encoding="utf-8") as f:
                json.dump(self.latest, f)
            with open("./data/history.json", "w", encoding="utf-8") as f:
                json.dump(self.history, f)

    def get_latest(self, location):
        return self.latest[location]

    def get_latest_by_api_key(self, location):
        return self.get_latest(self.api_key_mapping[location])