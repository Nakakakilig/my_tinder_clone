import os
import sys

from pydantic import BaseModel

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../"))
)  # for common
from common.enums import Gender


class DeckItem(BaseModel):
    profile_id: int
    first_name: str
    last_name: str
    gender: Gender
    age: int
    location: str


class DeckRead(BaseModel):
    profile_id: int
    cards: list[DeckItem]
