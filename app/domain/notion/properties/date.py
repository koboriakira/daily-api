from dataclasses import dataclass
from app.domain.notion.properties.property import Property
from typing import Optional


@dataclass
class Date(Property):
    start: Optional[str] = None
    end: Optional[str] = None
    time_zone: Optional[str] = None
    type: str = "date"

    def __init__(self, name: str, id: str, start: str, end: str, time_zone: str):
        self.id = id
        self.name = name
        self.start = start
        self.end = end
        self.time_zone = time_zone

    @staticmethod
    def of(name: str, param: dict) -> "Date":
        return Date(
            name=name,
            id=param["id"],
            start=param["date"]["start"],
            end=param["date"]["end"],
            time_zone=param["date"]["time_zone"]
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
