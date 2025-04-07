from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import ValidationError

from application.services.preference import PreferenceService
from domain.exceptions import PreferenceForProfileNotFoundError, PreferenceNotFoundError
from presentation.dependencies.preference import get_preference_service
from presentation.mappers.preference import (
    preference_to_read_schema,
    preferences_to_read_schema_list,
)
from presentation.schemas.preference import PreferenceReadSchema

router = APIRouter(tags=["preferences"])


@router.get("/")
async def get_preferences(
    preference_service: Annotated[PreferenceService, Depends(get_preference_service)],
) -> list[PreferenceReadSchema]:
    try:
        preferences = await preference_service.get_preferences()
        if not preferences:
            raise PreferenceNotFoundError()
        return preferences_to_read_schema_list(preferences)
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)) from e
    except PreferenceNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e


@router.get("/{preference_id}")
async def get_preference_by_id(
    preference_id: int,
    preference_service: Annotated[PreferenceService, Depends(get_preference_service)],
) -> PreferenceReadSchema:
    try:
        preference = await preference_service.get_preference_by_id(preference_id)
        if not preference:
            raise PreferenceNotFoundError(preference_id)
        return preference_to_read_schema(preference)
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)) from e
    except PreferenceNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e


@router.get("/profile/{profile_id}")
async def get_preference_by_profile_id(
    profile_id: int,
    preference_service: Annotated[PreferenceService, Depends(get_preference_service)],
) -> PreferenceReadSchema:
    try:
        preference = await preference_service.get_preference_by_profile_id(profile_id)
        if not preference:
            raise PreferenceForProfileNotFoundError(profile_id)
        return preference_to_read_schema(preference)

    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)) from e
    except PreferenceNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e
