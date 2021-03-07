import json
from copy import deepcopy

from models.data_entry import DataEntry


class DataWriter:

    def __init__(self):
        pass

    def update(self, entry: DataEntry):
        """
        Updates the latest dataset with the data entry if it is a new entry
        :return:
        """

        # load latest data:
        with open("./data/stats_latest.json", "r", encoding="utf-8") as f:
            latest = json.load(f)

        latest_entry = latest.get(entry.location)
        if latest_entry is None:
            entry_dict = entry.to_dict()
            del entry_dict["location"]
            latest[entry.location] = entry_dict
            with open("./data/stats_latest.json", "w", encoding="utf-8") as f:
                json.dump(latest, f)
        else:
            latest_copy = deepcopy(latest_entry)
            #  check if there are any changes:
            no_diffs = True
            for key in latest_entry.keys():
                if key == "timestamp":
                    continue
                if latest_entry[key] != getattr(entry, key):
                    no_diffs = False
                    latest_entry[key] = getattr(entry, key)

            if no_diffs is False:
                # save the changes:
                with open("./data/stats_latest.json", "w", encoding="utf-8") as f:
                    json.dump(latest, f)

                # add latest to history:
                self._add_to_history(entry.location, latest_copy)

    def _add_to_history(self, location, entry):
        with open("./data/stats_history.json", "r", encoding="utf-8") as f:
            history = json.load(f)
        if history[location] is None:
            history[location] = []
        history[location].append(entry)
        with open("./data/stats_history.json", "w", encoding="utf-8") as f:
            json.dump(history, f)
