from pydantic import BaseModel


class Photo(BaseModel):
    id: int
    profile_id: int
    url: str
