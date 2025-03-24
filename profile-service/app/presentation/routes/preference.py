from application.services.preference import PreferenceService
from application.schemas.preference import PreferenceCreateSchema, PreferenceReadSchema
from fastapi import APIRouter, Depends
from presentation.dependencies.preference import get_preference_service

router = APIRouter(tags=["preferences"])


@router.get("/", response_model=list[PreferenceReadSchema])
async def get_preferences(
    preference_service: PreferenceService = Depends(get_preference_service),
):
    return await preference_service.get_preferences()


@router.post("/", response_model=PreferenceReadSchema)
async def create_preference(
    preference_create: PreferenceCreateSchema,
    preference_service: PreferenceService = Depends(get_preference_service),
    # TODO in future:  user_id: UUID = Depends(get_user_id_from_JWT_token)
) -> PreferenceReadSchema:
    return await preference_service.create_preference(preference_create)


@router.get("/{preference_id}", response_model=PreferenceReadSchema)
async def get_preference_by_id(
    preference_id: int,
    preference_service: PreferenceService = Depends(get_preference_service),
) -> PreferenceReadSchema:
    return await preference_service.get_preference_by_id(preference_id)


@router.get("/profile/{profile_id}", response_model=PreferenceReadSchema)
async def get_preference_by_profile_id(
    profile_id: int,
    preference_service: PreferenceService = Depends(get_preference_service),
) -> PreferenceReadSchema:
    return await preference_service.get_preference_by_profile_id(profile_id)


# TODO: when want to update preference - generate new deck
# TODO: # @router.put("/update/{preference_id}", response_model=PreferenceRead)
