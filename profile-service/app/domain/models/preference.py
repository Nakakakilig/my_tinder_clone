from dataclasses import dataclass
from datetime import datetime

from domain.enums import Gender


@dataclass
class Preference:
    profile_id: int
    gender: Gender
    age: int
    radius: int
    updated_at: datetime
