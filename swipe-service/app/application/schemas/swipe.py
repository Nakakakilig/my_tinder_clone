from datetime import datetime

from pydantic import BaseModel


class SwipeBaseSchema(BaseModel):
    profile_id_1: int
    profile_id_2: int
    decision_1: bool | None = None
    decision_2: bool | None = None


class SwipeCreateSchema(SwipeBaseSchema):
    pass


class SwipeReadSchema(SwipeBaseSchema):
    id: int
    created_at: datetime
    updated_at: datetime
