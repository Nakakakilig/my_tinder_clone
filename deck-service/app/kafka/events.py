from typing import Any, Literal, TypedDict

from app.core.db.db_helper import db_helper
from app.core.schemas.preferences import PreferenceCreate
from app.core.schemas.profile import ProfileCreate
from app.services.preference import create_preference_service
from app.services.profile import create_profile_service


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
        await create_profile_service(session, profile_data)


async def handle_preference_created(
    data: DataType,
):
    async with db_helper.session_factory() as session:
        preference_data: PreferenceCreate = PreferenceCreate(**data)
        await create_preference_service(session, preference_data)
