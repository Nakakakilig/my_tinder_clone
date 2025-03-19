import asyncio

from app.utils.fake_data.create_swipes import create_swipes_between_profiles

N_PROFILES = 100


async def main():
    await create_swipes_between_profiles(N_PROFILES)


if __name__ == "__main__":
    asyncio.run(main())
