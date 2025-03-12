from pydantic import BaseModel

from app.core.schemas.enums import Gender


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
