from typing import Any, Literal, TypedDict
from core.db.db_helper import db_helper
from crud import profile as profile_crud
from crud import preference as preference_crud

from core.schemas.profile import ProfileCreate
from core.schemas.preferences import PreferenceCreate


class Event(TypedDict):
    event_type: Literal[
        "profile_created",
        "preference_created",
    ]
    data: dict[str, Any]
    timestamp: str


DataType = Event["data"]


async def handle_event(event: Event):
    event_type = event.get("event_type")
    data = event.get("data")
    if not event_type or not data:
        return

    if event_type == "profile_created":
        await handle_profile_created(data=data)
    elif event_type == "preference_created":
        await handle_preference_created(data)


async def handle_profile_created(
    data: DataType,
):
    async with db_helper.session_factory() as session:
        profile_data: ProfileCreate = ProfileCreate(**data)

        await profile_crud.create_profile(
            session,
            profile_data,
        )


async def handle_preference_created(
    data: DataType,
):
    async with db_helper.session_factory() as session:
        preference_data: PreferenceCreate = PreferenceCreate(**data)

        await preference_crud.create_preference(
            session,
            preference_data,
        )
