from typing import Annotated

from fastapi import APIRouter, Depends

from application.schemas.preference import PreferenceRead
from application.services.preference import PreferenceService
from presentation.dependencies.preference import get_preference_service

router = APIRouter(tags=["preferences"])


@router.get("/", response_model=list[PreferenceRead])
async def get_preferences(
    preference_service: Annotated[PreferenceService, Depends(get_preference_service)],
):
    return await preference_service.get_preferences()


@router.get("/{preference_id}", response_model=PreferenceRead)
async def get_preference_by_id(
    preference_id: int,
    preference_service: Annotated[PreferenceService, Depends(get_preference_service)],
) -> PreferenceRead:
    return await preference_service.get_preference_by_id(preference_id)


@router.get("/profile/{profile_id}", response_model=PreferenceRead)
async def get_preference_by_profile_id(
    profile_id: int,
    preference_service: Annotated[PreferenceService, Depends(get_preference_service)],
) -> PreferenceRead:
    return await preference_service.get_preference_by_profile_id(profile_id)
