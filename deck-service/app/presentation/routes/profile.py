from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import ValidationError

from application.schemas.profile import ProfileReadSchema
from application.services.profile import ProfileService
from domain.exceptions import ProfileNotFoundError
from presentation.dependencies.profile import get_profile_service
from presentation.mappers.profile import profile_to_read_schema, profiles_to_read_schema_list

router = APIRouter(tags=["profiles"])


@router.get("/")
async def get_profiles(
    profile_service: Annotated[ProfileService, Depends(get_profile_service)],
) -> list[ProfileReadSchema]:
    try:
        profiles = await profile_service.get_profiles()
        if not profiles:
            raise ProfileNotFoundError()
        return profiles_to_read_schema_list(profiles)
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)) from e
    except ProfileNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e


@router.get("/{profile_id}")
async def get_profile(
    profile_id: int,
    profile_service: Annotated[ProfileService, Depends(get_profile_service)],
) -> ProfileReadSchema:
    try:
        profile = await profile_service.get_profile_by_id(profile_id)
        if not profile:
            raise ProfileNotFoundError(profile_id)
        return profile_to_read_schema(profile)
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)) from e
    except ProfileNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e
