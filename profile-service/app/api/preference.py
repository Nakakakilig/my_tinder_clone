from fastapi import APIRouter

from app.api.deps import db_dependency
from app.core.schemas.preferences import PreferenceCreate, PreferenceRead
from app.services.preference import (
    create_preference_service,
    get_preference_service,
    get_preferences_service,
)

router = APIRouter(tags=["preferences"])


@router.get("/", response_model=list[PreferenceRead])
async def get_preferences(
    session: db_dependency,
):
    return await get_preferences_service(session)


@router.post("/", response_model=PreferenceRead)
async def create_preference(
    session: db_dependency,
    preference_create: PreferenceCreate,
    # TODO in future:  user_id: UUID = Depends(get_user_id_from_JWT_token)
) -> PreferenceRead:
    return await create_preference_service(session, preference_create)


@router.get("/{preference_id}", response_model=PreferenceRead)
async def get_preference(
    session: db_dependency,
    preference_id: int,
) -> PreferenceRead:
    return await get_preference_service(session, preference_id)


# TODO: when want to update preference - generate new deck
# TODO: # @router.put("/update/{preference_id}", response_model=PreferenceRead)
