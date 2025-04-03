from dataclasses import dataclass
from datetime import datetime


@dataclass
class Swipe:
    profile_id_1: int  # id of the profile that swiped
    profile_id_2: int  # id of the profile that swiped
    id: int | None = None
    decision_1: bool | None = None  # decision of the profile_1 about profile_2
    decision_2: bool | None = None  # decision of the profile_2 about profile_1
    created_at: datetime | None = None
    updated_at: datetime | None = None
