from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from domain.exceptions import (
    SwipeAlreadyExistsError,
    SwipeCreateError,
    SwipeNotFoundError,
)


def add_exception_handler(app: FastAPI) -> FastAPI:
    @app.exception_handler(SwipeNotFoundError)
    async def _(request: Request, exc: SwipeNotFoundError):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": str(exc)},
        )

    @app.exception_handler(SwipeAlreadyExistsError)
    async def _(request: Request, exc: SwipeAlreadyExistsError):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"detail": str(exc)},
        )

    @app.exception_handler(SwipeCreateError)
    async def _(request: Request, exc: SwipeCreateError):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": str(exc)},
        )

    @app.exception_handler(ConnectionRefusedError)
    async def _(request: Request, exc: ConnectionRefusedError):
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"detail": "Connection to DB refused"},
        )

    @app.exception_handler(Exception)
    async def _(request: Request, exc: Exception):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Internal server error."},
        )

    return app
