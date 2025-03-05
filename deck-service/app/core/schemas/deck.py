import os
import sys

from pydantic import BaseModel

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../"))
)  # for common
from common.enums import Gender


class MatchCard(BaseModel):  # profile card of a potential match
    profile_id: int
    first_name: str
    last_name: str
    gender: Gender
    age: int
    distance_km: float


class MatchDeck(BaseModel):
    profile_id: int
    candidates: list[MatchCard]
