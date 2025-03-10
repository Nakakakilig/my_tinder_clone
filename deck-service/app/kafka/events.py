from core.db.db_helper import db_helper
from crud import profile as profile_crud

from core.schemas.profile import ProfileCreate


async def handle_event(event: dict):
    print(f"I GET SOME EVENT: {event = }")
    event_type = event.get("event_type")
    data = event.get("data")

    if event_type == "profile_created":
        print('I SAW "PROFILE_CREATED" EVENT')
        await handle_profile_created(data=data)


async def handle_profile_created(
    data: dict,
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
