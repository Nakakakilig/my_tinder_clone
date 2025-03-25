from typing import AsyncGenerator

from infrastructure.db.db_helper import db_helper
from sqlalchemy.ext.asyncio import AsyncSession


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async for session in db_helper.session_getter():
        yield session
