from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.db_helper import db_helper

db_dependency = Annotated[AsyncSession, Depends(db_helper.session_getter)]
