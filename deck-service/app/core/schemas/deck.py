from core.schemas.enums import Gender
from pydantic import BaseModel


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
