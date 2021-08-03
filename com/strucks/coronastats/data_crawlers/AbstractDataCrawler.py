from abc import abstractmethod, ABC

from com.strucks.coronastats.data_manager import DataManager
from com.strucks.coronastats.models import OverviewDataRow


class AbstractDataCrawler(ABC):

    def __init__(self, url):
        self.url = url
        self.latest = None
        print("successfully created %s crawler" % self.get_location())

    @abstractmethod
    def refresh(self) -> OverviewDataRow:
        raise NotImplementedError()

    @abstractmethod
    def get_location(self) -> str:
        raise NotImplementedError()

    def get_latest(self) -> OverviewDataRow:
        return self.latest

    def update(self, entry):
        dm: DataManager = DataManager.instance()
        dm.update(self.get_location(), entry)
