from dataclasses import dataclass
from datetime import datetime


@dataclass
class User:
    username: str
    id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
