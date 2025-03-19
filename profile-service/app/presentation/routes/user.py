from application.schemas.user import UserCreate, UserRead
from application.services.user import UserService
from fastapi import APIRouter, Depends
from presentation.dependencies.user import get_user_service

router = APIRouter(tags=["users"])


@router.post("/", response_model=UserRead)
async def create_user(
    user_create: UserCreate,
    user_service: UserService = Depends(get_user_service),
) -> UserRead:
    # TODO: somehow create profile after user creation
    user = await user_service.create_user(user_create)
    return user


@router.get("/", response_model=list[UserRead])
async def get_users(
    user_service: UserService = Depends(get_user_service),
) -> list[UserRead]:
    return await user_service.get_users()


@router.get("/{user_id}", response_model=UserRead)
async def get_user(
    user_id: int,
    user_service: UserService = Depends(get_user_service),
) -> UserRead:
    return await user_service.get_user_by_id(user_id)
