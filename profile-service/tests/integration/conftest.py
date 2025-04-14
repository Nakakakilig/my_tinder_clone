import asyncio
from collections.abc import AsyncGenerator
from typing import Any

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.infrastructure.db.base import Base

DATABASE_URL = "postgresql+asyncpg://user-test:password-test@localhost:5400/profile-test"


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def db_engine():
    engine = create_async_engine(DATABASE_URL, echo=True)

    alembic_cfg = Config("app/alembic.ini")
    alembic_cfg.set_main_option("script_location", "app/alembic")
    alembic_cfg.set_main_option("sqlalchemy.url", DATABASE_URL)

    async with engine.begin() as conn:

        def do_migration(connection: Any) -> None:
            command.upgrade(alembic_cfg, "head")

        await conn.run_sync(do_migration)

    yield engine

    async with engine.begin() as conn:
        # def do_downgrade(connection: Any) -> None:
        #     command.downgrade(alembic_cfg, "base")

        # await conn.run_sync(do_downgrade)
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest.fixture(scope="function")
async def db_session(db_engine: AsyncEngine) -> AsyncGenerator[AsyncSession, None]:
    session_factory = async_sessionmaker(db_engine, expire_on_commit=False)
    async with session_factory() as session:
        yield session


# @pytest.fixture
# async def db_session(db_engine: AsyncEngine) -> AsyncGenerator[AsyncConnection, None]:
#     async with db_engine.begin() as conn:
#         yield conn


# @pytest.fixture
# async def kafka_producer():
#     producer = KafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
#     await producer.start()
#     yield producer
#     await producer.stop()
