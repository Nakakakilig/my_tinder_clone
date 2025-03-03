import asyncio

from create_profiles import create_multiple_profiles
from create_users import create_multiple_users
from create_preferences import create_multiple_preferences

N_USERS = 100


async def main():
    await asyncio.gather(
        create_multiple_users(N_USERS),
        create_multiple_profiles(N_profiles=N_USERS),
        create_multiple_preferences(N_preferences=N_USERS),
    )


asyncio.run(main())
