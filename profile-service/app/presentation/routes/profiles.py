from application.schemas.profile import ProfileCreateSchema, ProfileReadSchema
from application.services.profile import ProfileService
from fastapi import APIRouter, Depends
from presentation.dependencies.profile import get_profile_service

router = APIRouter(tags=["profiles"])


@router.get("/", response_model=list[ProfileReadSchema])
async def get_profiles(
    profile_service: ProfileService = Depends(get_profile_service),
):
    return await profile_service.get_profiles()


@router.post("/", response_model=ProfileReadSchema)
async def create_profile(
    profile_create: ProfileCreateSchema,
    profile_service: ProfileService = Depends(get_profile_service),
    # TODO in future:  user_id: UUID = Depends(get_user_id_from_JWT_token)
) -> ProfileReadSchema:
    return await profile_service.create_profile(profile_create)


@router.get("/{profile_id}", response_model=ProfileReadSchema)
async def get_profile(
    profile_id: int,
    profile_service: ProfileService = Depends(get_profile_service),
) -> ProfileReadSchema:
    return await profile_service.get_profile_by_id(profile_id)


@router.get("/user/{user_id}", response_model=ProfileReadSchema)
async def get_profile_by_user_id(
    user_id: int,
    profile_service: ProfileService = Depends(get_profile_service),
) -> ProfileReadSchema:
    return await profile_service.get_profile_by_user_id(user_id)
