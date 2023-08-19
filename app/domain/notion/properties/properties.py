from abc import ABCMeta, abstractmethod
from typing import Optional
from app.domain.notion.properties.property import Property
from dataclasses import dataclass


@dataclass(frozen=True)
class Properties:
    values: list[Property]

    def __dict__(self):
        result = {}
        for value in self.values:
            result = {**result, **value.__dict__()}
        return result
