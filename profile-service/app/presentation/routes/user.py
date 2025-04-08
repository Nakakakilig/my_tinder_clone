from fastapi import APIRouter, Depends

from application.schemas.user import UserCreateSchema, UserReadSchema
from application.services.user import UserService
from presentation.dependencies.user import get_user_service

router = APIRouter(tags=["users"])


@router.post("/", response_model=UserReadSchema)
async def create_user(
    user_create: UserCreateSchema,
    user_service: UserService = Depends(get_user_service),
) -> UserReadSchema:
    # TODO: somehow create profile after user creation
    user = await user_service.create_user(user_create)
    return user


@router.get("/", response_model=list[UserReadSchema])
async def get_users(
    user_service: UserService = Depends(get_user_service),
) -> list[UserReadSchema]:
    return await user_service.get_users()


@router.get("/{user_id}", response_model=UserReadSchema)
async def get_user(
    user_id: int,
    user_service: UserService = Depends(get_user_service),
) -> UserReadSchema:
    return await user_service.get_user_by_id(user_id)
