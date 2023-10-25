from dataclasses import dataclass
from typing import Optional


@dataclass
class Icon():
    type: str
    emoji: Optional[str] = None

    @staticmethod
    def of(param: dict) -> "Icon":
        return Icon(
            type=param["type"],
            emoji=param["emoji"] if "emoji" in param else None
        )
