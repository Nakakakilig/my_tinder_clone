from fastapi import Query
from pydantic import BaseModel

from config.settings import settings


class PaginationParams(BaseModel):
    limit: int = Query(
        default=settings.pagination.default_limit,
        ge=settings.pagination.min_limit,
        le=settings.pagination.max_limit,
    )
    offset: int = Query(
        default=settings.pagination.default_offset,
        ge=settings.pagination.min_offset,
        le=settings.pagination.max_offset,
    )
