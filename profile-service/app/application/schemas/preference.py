from datetime import datetime

from domain.enums import EventType, Gender
from pydantic import BaseModel


class PreferenceBase(BaseModel):
    profile_id: int
    gender: Gender
    age: int
    radius: int


class PreferenceCreate(PreferenceBase):
    pass


class PreferenceRead(PreferenceBase):
    id: int
    updated_at: datetime


class PreferenceCreatedEvent(PreferenceBase):
    event_type: str = EventType.PREFERENCE_CREATED.value
    occurred_at: datetime
