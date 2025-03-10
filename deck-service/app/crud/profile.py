from core.models.profile import Profile
from core.schemas.profile import ProfileCreate
from sqlalchemy.ext.asyncio import AsyncSession


async def create_profile(
    session: AsyncSession,
    profile_create: ProfileCreate,
) -> Profile:
    print("CREATING PROFILE")
    profile = Profile(**profile_create.model_dump())
    session.add(profile)
    await session.commit()
    await session.refresh(profile)
    print("PROFILE CREATED SUCCESSFULLY")
    return profile
