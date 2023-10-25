from dataclasses import dataclass
from typing import Optional


@dataclass
class Parent():
    type: str
    workspace: Optional[bool] = None
