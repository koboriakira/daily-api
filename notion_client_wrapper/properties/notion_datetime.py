from dataclasses import dataclass
from datetime import datetime as DatetimeObject
from datetime import timedelta
from enum import Enum


class TimeKind(Enum):
    CREATED_TIME = "created_time"
    LAST_EDITED_TIME = "last_edited_time"


@dataclass
class NotionDatetime:
    value: DatetimeObject
    kind: TimeKind

    @classmethod
    def created_time(cls, value: str) -> "NotionDatetime":
        datetime = DatetimeObject.fromisoformat(value[:-1])
        datetime += timedelta(hours=9)
        return cls(
            value=datetime,
            kind=TimeKind.CREATED_TIME,
        )

    @classmethod
    def last_edited_time(cls, value: str) -> "NotionDatetime":
        datetime = cls.__to_datetime(value)
        return cls(
            value=datetime,
            kind=TimeKind.LAST_EDITED_TIME,
        )

    @classmethod
    def __to_datetime(cls, value: str) -> DatetimeObject:
        try:
            datetime = DatetimeObject.fromisoformat(value[:-1])
            # FIXME: 日本以外にも対応したい
            datetime += timedelta(hours=9)
            return datetime
        except Exception as e:
            raise Exception(f"Invalid datetime format: {value} {e}")

    def __dict__(self):
        return {self.kind.value: self.value.isoformat() + "Z"}
