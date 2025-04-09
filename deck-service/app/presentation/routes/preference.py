from typing import Annotated

from fastapi import APIRouter, Depends, Path

from domain.exceptions import PreferenceForProfileNotFoundError, PreferenceNotFoundError
from presentation.dependencies.preference import get_preference_service
from presentation.mappers.preference import (
    preference_to_read_schema,
    preferences_to_read_schema_list,
)
from presentation.routes.common import PaginationParams
from presentation.schemas.preference import PreferenceReadSchema
from use_cases.preference import PreferenceService

router = APIRouter(tags=["preferences"])


@router.get("/")
async def get_preferences(
    pagination: Annotated[PaginationParams, Depends()],
    preference_service: Annotated[PreferenceService, Depends(get_preference_service)],
) -> list[PreferenceReadSchema]:
    preferences = await preference_service.get_preferences(pagination.limit, pagination.offset)
    if not preferences:
        raise PreferenceNotFoundError()
    return preferences_to_read_schema_list(preferences)


@router.get("/{preference_id}")
async def get_preference_by_id(
    preference_id: Annotated[int, Path(gt=0)],
    preference_service: Annotated[PreferenceService, Depends(get_preference_service)],
) -> PreferenceReadSchema:
    preference = await preference_service.get_preference_by_id(preference_id)
    if not preference:
        raise PreferenceNotFoundError(preference_id)
    return preference_to_read_schema(preference)


@router.get("/profile/{profile_id}")
async def get_preference_by_profile_id(
    profile_id: Annotated[int, Path(gt=0)],
    preference_service: Annotated[PreferenceService, Depends(get_preference_service)],
) -> PreferenceReadSchema:
    preference = await preference_service.get_preference_by_profile_id(profile_id)
    if not preference:
        raise PreferenceForProfileNotFoundError(profile_id)
    return preference_to_read_schema(preference)
