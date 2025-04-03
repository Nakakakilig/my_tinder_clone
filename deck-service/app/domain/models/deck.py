from pydantic import BaseModel

from domain.enums import Gender


class MatchCard(BaseModel):  # profile card of a potential match
    profile_id: int  # profile id of the potential match
    first_name: str  # first name of the potential match
    last_name: str  # last name of the potential match
    gender: Gender  # gender of the potential match
    age: int  # age of the potential match
    distance_km: float  # distance in km between the user and the potential match


class MatchDeck(BaseModel):
    profile_id: int  # profile id of the user
    candidates: list[MatchCard]  # list of potential matches
