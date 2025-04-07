from datetime import datetime

from pydantic import BaseModel, Field, model_validator


class SwipeBaseSchema(BaseModel):
    profile_id_1: int = Field(..., gt=0)
    profile_id_2: int = Field(..., gt=0)
    decision_1: bool | None = None
    decision_2: bool | None = None


class SwipeCreateSchema(SwipeBaseSchema):
    @model_validator(mode="after")
    def swap_profile_ids(self):
        """
        Swap profile IDs if profile_id_2 is less than profile_id_1.
        Also swap decisions.
        It helps to avoid duplicate swipes.
        """
        if self.profile_id_2 < self.profile_id_1:
            self.profile_id_1, self.profile_id_2 = self.profile_id_2, self.profile_id_1
            self.decision_1, self.decision_2 = self.decision_2, self.decision_1
        return self


class SwipeReadSchema(SwipeBaseSchema):
    id: int
    created_at: datetime
    updated_at: datetime
