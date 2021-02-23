

class DataEntry:

    def __init__(self, location: str, incidence: float, active: int, deaths: int, cured: int, total: int, timestamp: str):
        self.location = location
        self.incidence = incidence
        self.active = active
        self.deaths = deaths
        self.cured = cured
        self.total = total
        self.timestamp = timestamp

    def to_dict(self):
        return {
            "location": self.location,
            "incidence": self.incidence,
            "active": self.active,
            "deaths": self.deaths,
            "cured": self.cured,
            "total": self.total,
            "timestamp": self.timestamp
        }