from dataclasses import dataclass
from datetime import datetime

from domain.enums import Gender


@dataclass
class Profile:
    id: int
    user_id: int
    first_name: str
    last_name: str
    gender: Gender
    age: int
    geo_latitude: float
    geo_longitude: float
    created_at: datetime
    updated_at: datetime
