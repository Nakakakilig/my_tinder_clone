from typing import Annotated

from fastapi import APIRouter, Depends, Path

from domain.models.preference import Preference
from presentation.dependencies.preference import get_preference_service
from presentation.mappers.preference import (
    preference_to_read_schema,
    preferences_to_read_schema_list,
)
from presentation.routes.common import PaginationParams
from presentation.schemas.preference import PreferenceCreateSchema, PreferenceReadSchema
from use_cases.preference import PreferenceService

router = APIRouter(tags=["preferences"])


@router.get("/")
async def get_preferences(
    preference_service: Annotated[PreferenceService, Depends(get_preference_service)],
    pagination: Annotated[PaginationParams, Depends(PaginationParams)],
) -> list[PreferenceReadSchema] | None:
    preferences = await preference_service.get_preferences(pagination.limit, pagination.offset)
    if not preferences:
        return None
    return preferences_to_read_schema_list(preferences)


@router.post("/")
async def create_preference(
    preference_create: PreferenceCreateSchema,
    preference_service: Annotated[PreferenceService, Depends(get_preference_service)],
    # TODO in future:  user_id: UUID = Depends(get_user_id_from_JWT_token)
) -> PreferenceReadSchema:
    preference_model = Preference(**preference_create.model_dump())
    preference = await preference_service.create_preference(preference_model)
    return preference_to_read_schema(preference)


@router.get("/{preference_id}")
async def get_preference_by_id(
    preference_id: Annotated[int, Path(gt=0)],
    preference_service: Annotated[PreferenceService, Depends(get_preference_service)],
) -> PreferenceReadSchema | None:
    preference = await preference_service.get_preference_by_id(preference_id)
    if not preference:
        return None
    return preference_to_read_schema(preference)


@router.get("/profile/{profile_id}")
async def get_preference_by_profile_id(
    profile_id: Annotated[int, Path(gt=0)],
    preference_service: Annotated[PreferenceService, Depends(get_preference_service)],
) -> PreferenceReadSchema | None:
    preference = await preference_service.get_preference_by_profile_id(profile_id)
    if not preference:
        return None
    return preference_to_read_schema(preference)


# TODO: when want to update preference - generate new deck
# TODO: # @router.put("/update/{preference_id}", response_model=PreferenceRead)
