from core.schemas.preferences import PreferenceCreate, PreferenceRead
from crud import preferences as preferences_crud
from fastapi import APIRouter, HTTPException

from api.deps import db_dependency

router = APIRouter(tags=["preferences"])


@router.get("/", response_model=list[PreferenceRead])
async def get_preferences(
    session: db_dependency,
):
    preferences = await preferences_crud.get_all_preferences(session=session)
    if not preferences:
        raise HTTPException(status_code=404, detail="No any preferences found")
    return preferences


@router.post("/", response_model=PreferenceRead)
async def create_preference(
    session: db_dependency,
    preference_create: PreferenceCreate,
    # TODO in future:  user_id: UUID = Depends(get_user_id_from_JWT_token)
) -> PreferenceRead:
    preference = await preferences_crud.create_preference(
        session=session,
        preference_create=preference_create,
    )
    if not preference:
        raise HTTPException(status_code=404, detail="Preference not create")
    return preference


@router.get("/{preference_id}", response_model=PreferenceRead)
async def get_preference(
    session: db_dependency,
    preference_id: int,
) -> PreferenceRead:
    preference = await preferences_crud.get_preference(
        session=session,
        preference_id=preference_id,
    )
    if not preference:
        raise HTTPException(status_code=404, detail="There is no such preference")
    return preference


# TODO: when want to update preference - generate new deck
# TODO: # @router.put("/update/{preference_id}", response_model=PreferenceRead)
