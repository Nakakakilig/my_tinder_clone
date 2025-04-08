from typing import Annotated

from fastapi import APIRouter, Depends

from domain.models.user import User
from presentation.dependencies.user import get_user_service
from presentation.mappers.user import user_to_read_schema, users_to_read_schema_list
from presentation.routes.common import PaginationParams
from presentation.schemas.user import UserCreateSchema, UserReadSchema
from use_cases.user import UserService

router = APIRouter(tags=["users"])


@router.post("/")
async def create_user(
    user_create: UserCreateSchema,
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> UserReadSchema:
    # TODO: somehow create profile after user creation
    user_model = User(**user_create.model_dump())
    user = await user_service.create_user(user_model)
    return user_to_read_schema(user)


@router.get("/")
async def get_users(
    user_service: Annotated[UserService, Depends(get_user_service)],
    pagination: Annotated[PaginationParams, Depends(PaginationParams)],
) -> list[UserReadSchema] | None:
    users = await user_service.get_users(pagination.limit, pagination.offset)
    if users is None:
        return None
    return users_to_read_schema_list(users)


@router.get("/{user_id}")
async def get_user(
    user_id: int,
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> UserReadSchema | None:
    user = await user_service.get_user_by_id(user_id)
    if user is None:
        return None
    return user_to_read_schema(user)


@router.get("/username/{username}")
async def get_user_by_username(
    username: str,
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> UserReadSchema | None:
    user = await user_service.get_user_by_username(username)
    if user is None:
        return None
    return user_to_read_schema(user)
