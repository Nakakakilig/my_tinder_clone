from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from core.db.enums import Gender


class ProfileBase(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    gender: Gender
    geo_latitude: float
    geo_longitude: float
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class ProfileCreate(ProfileBase):
    pass


class ProfileRead(ProfileBase):
    id: int
