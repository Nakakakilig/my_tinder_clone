from typing import Annotated

import logging
from fastapi import APIRouter, Depends, Path

from domain.models.user import User
from presentation.dependencies.user import get_user_service
from presentation.mappers.user import user_to_read_schema, users_to_read_schema_list
from presentation.routes.common import PaginationParams
from presentation.schemas.user import UserCreateSchema, UserReadSchema
from use_cases.user import UserService

logger = logging.getLogger(__name__)
router = APIRouter(tags=["users"])


@router.post("/")
async def create_user(
    user_create: UserCreateSchema,
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> UserReadSchema:
    # TODO: somehow create profile after user creation
    logger.info("Incoming request: create_user")
    user_model = User(**user_create.model_dump())
    user = await user_service.create_user(user_model)
    user_read = user_to_read_schema(user)
    logger.info("Created user with id %d", user_read.id)
    return user_read


@router.get("/")
async def get_users(
    user_service: Annotated[UserService, Depends(get_user_service)],
    pagination: Annotated[PaginationParams, Depends(PaginationParams)],
) -> list[UserReadSchema] | None:
    logger.info(
        "Incoming request: get_users (limit=%d, offset=%d)",
        pagination.limit,
        pagination.offset,
    )
    users = await user_service.get_users(pagination.limit, pagination.offset)
    if users is None:
        return None
    users = users_to_read_schema_list(users)
    logger.info("Returning users")
    return users


@router.get("/{user_id}")
async def get_user(
    user_id: Annotated[int, Path(gt=0)],
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> UserReadSchema | None:
    logger.info("Incoming request: get_user (user_id=%d)", user_id)
    user = await user_service.get_user_by_id(user_id)
    if user is None:
        return None
    user_read = user_to_read_schema(user)
    logger.info("Returning user with id %d", user_read.id)
    return user_read


@router.get("/username/{username}")
async def get_user_by_username(
    username: Annotated[str, Path(min_length=1, max_length=20)],
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> UserReadSchema | None:
    logger.info("Incoming request: get_user_by_username (username=%s)", username)
    user = await user_service.get_user_by_username(username)
    if user is None:
        return None
    user_read = user_to_read_schema(user)
    logger.info("Returning user with id %d", user_read.id)
    return user_read
