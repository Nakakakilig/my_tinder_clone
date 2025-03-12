from fastapi import APIRouter

from app.api.deps import db_dependency
from app.core.schemas.user import UserCreate, UserRead
from app.crud import users as users_crud

router = APIRouter(tags=["users"])


@router.get("/get-all", response_model=list[UserRead])
async def get_users(
    session: db_dependency,
):
    users = await users_crud.get_all_users(session=session)
    return users


@router.post("/create", response_model=UserRead)
async def create_user(
    session: db_dependency,
    user_create: UserCreate,
) -> UserRead:
    user = await users_crud.create_user(
        session=session,
        user_create=user_create,
    )
    # TODO: somehow create profile after user creation
    return user


@router.get("/{user_id}", response_model=UserRead)
async def get_user(
    session: db_dependency,
    user_id: int,
) -> UserRead:
    user = await users_crud.get_user(session=session, user_id=user_id)
    return user
