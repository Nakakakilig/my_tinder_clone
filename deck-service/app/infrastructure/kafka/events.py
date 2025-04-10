from typing import Any, Literal, TypedDict

import logging

from domain.models.preference import Preference
from domain.models.profile import Profile
from infrastructure.db.db_helper import db_helper
from infrastructure.repositories_impl.preference import PreferenceRepositoryImpl
from infrastructure.repositories_impl.profile import ProfileRepositoryImpl
logger = logging.getLogger(__name__)


class Event(TypedDict):
    event_type: Literal[
        "profile_created",
        "preference_created",
    ]
    data: dict[str, Any]
    timestamp: str


async def handle_event(event: Event):
    event_type = event["event_type"]
    data = event["data"]
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
        logger.error(f"No handler found for event type: {event_type}")  # noqa: TRY003


async def handle_profile_created(
    data: dict[str, Any],
):
    logger.info("Handling profile created event")
    async with db_helper.session_factory() as session:
        profile_schema = ProfileCreateSchema(**data)
        profile = Profile(**profile_schema.model_dump())
        await ProfileRepositoryImpl(session).create_profile(profile)


async def handle_preference_created(
    data: dict[str, Any],
):
    async with db_helper.session_factory() as session:
        preference_schema = PreferenceCreateSchema(**data)
        preference = Preference(**preference_schema.model_dump())
        await PreferenceRepositoryImpl(session).create_preference(preference)
