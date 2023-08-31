from dataclasses import dataclass
from app.domain.notion.properties.property import Property
from typing import Optional
from datetime import datetime as DatetimeObject


@dataclass
class LastEditedTime(Property):
    value: DatetimeObject
    type: str = "last_edited_time"

    def __init__(self,
                 name: str,
                 value: DatetimeObject,
                 id: Optional[str] = None,):
        self.name = name
        self.value = value
        self.id = id

    @ staticmethod
    def of(name: str, param: dict) -> "LastEditedTime":
        return LastEditedTime(
            name=name,
            value=DatetimeObject.fromisoformat(param["last_edited_time"][:-1]),
            id=param["id"],
        )

    def __dict__(self):
        result = {
            "last_edited_time": self.value.isoformat() + "Z"
        }
        return {self.name: result}
