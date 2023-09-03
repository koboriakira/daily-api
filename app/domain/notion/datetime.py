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
    def from_page_block(cls, kind: TimeKind, block: dict) -> "NotionDatetime":
        datetime = DatetimeObject.fromisoformat(block[kind.value][:-1])
        datetime += timedelta(hours=9)
        return cls(
            value=datetime,
            kind=kind,
        )

    def __dict__(self):
        return {self.kind.value: self.value.isoformat() + "Z"}
