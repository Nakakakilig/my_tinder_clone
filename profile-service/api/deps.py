from typing import Annotated

from fastapi import Depends
from core.db.db_helper import db_helper
from sqlalchemy.ext.asyncio import AsyncSession

db_dependency = Annotated[AsyncSession, Depends(db_helper.session_getter)]
