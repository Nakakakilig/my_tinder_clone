from typing import Annotated

from fastapi import APIRouter, Depends

from application.schemas.user import UserCreateSchema, UserReadSchema
from application.services.user import UserService
from presentation.dependencies.user import get_user_service

router = APIRouter(tags=["users"])


@router.post("/")
async def create_user(
    user_create: UserCreateSchema,
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> UserReadSchema:
    # TODO: somehow create profile after user creation
    user = await user_service.create_user(user_create)
    return user


@router.get("/")
async def get_users(
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> list[UserReadSchema] | None:
    return await user_service.get_users()


@router.get("/{user_id}")
async def get_user(
    user_id: int,
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> UserReadSchema | None:
@router.get("/username/{username}")
async def get_user_by_username(
    username: str,
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> UserReadSchema | None:
    user = await user_service.get_user_by_username(username)
    if user is None:
        return None
    return user_to_read_schema(user)
