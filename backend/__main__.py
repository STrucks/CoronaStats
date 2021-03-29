import os
import re
import time
from pathlib import Path

from backend.corona_api_client import CoronaGlobalClient, CoronaLocalClient
from backend.data_writer import DataWriter
from models.data_entry import DataEntry

if __name__ == '__main__':
    # set the work dir to corona stats
    cwd = re.split("[\\\/]backend[\\\/]", __file__)[0]
    os.chdir(cwd)
    # set up data directory structure:
    Path("./data").mkdir(parents=True, exist_ok=True)
    try:
        with open("./data/stats_latest.json", "r", encoding="utf-8"):
            pass
    except FileNotFoundError:
        with open("./data/stats_latest.json", "w", encoding="utf-8") as f:
            f.write("{}")
    try:
        with open("./data/stats_history.json", "r", encoding="utf-8"):
            pass
    except FileNotFoundError:
        with open("./data/stats_history.json", "w", encoding="utf-8") as f:
            f.write("""{"world_wide": [], "germany": [], "oberhausen": [], "hannover": [], "kleve": []}""")
    try:
        with open("./data/stats_history.json", "r", encoding="utf-8"):
            pass
    except FileNotFoundError:
        with open("./data/population.json", "w", encoding="utf-8") as f:
            f.write("""{"world_wide": 7855000000, "germany": 83020000, "oberhausen": 211000, "kleve": 310000, "hannover": 532000, "kranenburg": 11000}""")

    # start the crawling life cycle:
    global_client = CoronaGlobalClient()
    local_client = CoronaLocalClient()
    data_writer = DataWriter()
    while True:
        for location in ["world_wide", "germany"]:
            try:
                data_entry: DataEntry = global_client.get_data(location)
                data_writer.update(data_entry)
            except Exception as e:
                print(str(e))

        for location in ["oberhausen", "hannover", "kleve", "kranenburg"]:
            try:
                data_entry: DataEntry = local_client.get_data(location)
                data_writer.update(data_entry)
            except Exception as e:
                print(str(e))
        local_client.refresh()

        time.sleep(900)
