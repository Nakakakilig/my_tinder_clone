from dataclasses import dataclass
from datetime import datetime

from domain.enums import Gender


@dataclass
class Profile:
    user_id: int
    first_name: str
    last_name: str
    gender: Gender
    age: int
    geo_latitude: float
    geo_longitude: float
    id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
