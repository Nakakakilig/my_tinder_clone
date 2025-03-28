from pydantic import BaseModel


class Swipe(BaseModel):
    profile_id_1: int
    profile_id_2: int
    decision_1: bool | None = None
    decision_2: bool | None = None
