from datetime import datetime

from domain.enums import EventType, Gender
from pydantic import BaseModel


class ProfileBase(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    gender: Gender
    age: int
    geo_latitude: float
    geo_longitude: float


class ProfileCreate(ProfileBase):
    pass


class ProfileRead(ProfileBase):
    id: int
    created_at: datetime
    updated_at: datetime


class ProfileCreatedEvent(ProfileBase):
    event_type: str = EventType.PROFILE_CREATED.value
    occurred_at: datetime
