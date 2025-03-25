from typing import Any, Literal, TypedDict

from application.schemas.preference import PreferenceCreate
from application.schemas.profile import ProfileCreate
from infrastructure.db.db_helper import db_helper
from infrastructure.repositories_impl.preference import PreferenceRepositoryImpl
from infrastructure.repositories_impl.profile import ProfileRepositoryImpl


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

    event_handlers = {
        "profile_created": handle_profile_created,
        "preference_created": handle_preference_created,
    }

    handler = event_handlers.get(event_type)
    if handler:
        await handler(data=data)
    else:
        raise ValueError(f"No handler found for event type: {event_type}")


async def handle_profile_created(
    data: DataType,
):
    async with db_helper.session_factory() as session:
        profile_data: ProfileCreate = ProfileCreate(**data)
        await ProfileRepositoryImpl(session).create_profile(profile_data)


async def handle_preference_created(
    data: DataType,
):
    async with db_helper.session_factory() as session:
        preference_data: PreferenceCreate = PreferenceCreate(**data)
        await PreferenceRepositoryImpl(session).create_preference(preference_data)
