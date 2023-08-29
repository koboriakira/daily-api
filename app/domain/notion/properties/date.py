from dataclasses import dataclass
from app.domain.notion.properties.property import Property
from typing import Optional
from datetime import date


@dataclass
class Date(Property):
    start: Optional[str] = None
    end: Optional[str] = None
    time_zone: Optional[str] = None
    type: str = "date"

    def __init__(self, name: str, id: Optional[str] = None, start: str = None, end: str = None, time_zone: str = None):
        self.name = name
        self.id = id
        self.start = start
        self.end = end
        self.time_zone = time_zone

    @staticmethod
    def of(name: str, param: dict) -> "Date":
        if param["date"] is None:
            return Date(name=name, id=param["id"])
        return Date(
            name=name,
            id=param["id"],
            start=param["date"]["start"],
            end=param["date"]["end"],
            time_zone=param["date"]["time_zone"]
        )

    @staticmethod
    def from_start_date(name: str, start_date: Optional[date] = None) -> "Date":
        return Date(
            name=name,
            start=start_date.isoformat() if start_date is not None else None,
        )

    @staticmethod
    def from_range(name: str, start: date, end: date) -> "Date":
        return Date(
            name=name,
            start=start.isoformat(),
            end=end.isoformat(),
        )

    def __dict__(self):
        return {
            self.name: {
                "type": self.type,
                "date": {
                    "start": self.start,
                    "end": self.end,
                    "time_zone": self.time_zone
                }
            }
        }
