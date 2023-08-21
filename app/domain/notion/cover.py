from dataclasses import dataclass
from typing import Optional


@dataclass
class Cover():
    type: str
    external_url: Optional[str] = None

    def __init__(self, type: str, external_url: Optional[str] = None):
        self.type = type
        self.external_url = external_url

    @staticmethod
    def from_external_url(external_url: str) -> "Cover":
        return Cover(
            type="external",
            external_url=external_url
        )

    def __dict__(self):
        result = {
            "type": self.type,
        }
        if self.external_url is not None:
            result["external"] = {
                "url": self.external_url
            }
        return result
