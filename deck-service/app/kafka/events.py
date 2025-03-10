from typing import Any, Literal, TypedDict
from core.db.db_helper import db_helper
from crud import profile as profile_crud

from core.schemas.profile import ProfileCreate


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
        print('I SAW "PROFILE_CREATED" EVENT')
        await handle_profile_created(data=data)


async def handle_profile_created(
    data: DataType,
):
    async with db_helper.session_factory() as session:
        print('START "PROFILE_CREATED" EVENT')
        profile_data: ProfileCreate = ProfileCreate(**data)
        print(f"{profile_data = }")

        await profile_crud.create_profile(
            session,
            profile_data,
        )
        print('END "PROFILE_CREATED" EVENT')
