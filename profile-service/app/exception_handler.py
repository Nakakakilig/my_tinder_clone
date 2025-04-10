import logging
from aiokafka.errors import KafkaConnectionError  # type: ignore
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from domain.exceptions import (
    PreferenceAlreadyExistsError,
    PreferenceCreateError,
    PreferenceNotFoundError,
    ProfileAlreadyExistsError,
    ProfileCreateError,
    ProfileNotFoundError,
    UserAlreadyExistsError,
    UserCreateError,
    UserNotFoundError,
)

logger = logging.getLogger(__name__)


def add_exception_handler(app: FastAPI) -> FastAPI:
    @app.exception_handler(ProfileNotFoundError)
    async def _(request: Request, exc: ProfileNotFoundError):
        logger.exception("Profile not found error: %s", exc)
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": str(exc)},
        )

    @app.exception_handler(ProfileAlreadyExistsError)
    async def _(request: Request, exc: ProfileAlreadyExistsError):
        logger.exception("Profile already exists error: %s", exc)
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"detail": str(exc)},
        )

    @app.exception_handler(ProfileCreateError)
    async def _(request: Request, exc: ProfileCreateError):
        logger.exception("Profile create error: %s", exc)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": str(exc)},
        )

    @app.exception_handler(PreferenceNotFoundError)
    async def _(request: Request, exc: PreferenceNotFoundError):
        logger.exception("Preference not found error: %s", exc)
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": str(exc)},
        )

    @app.exception_handler(PreferenceCreateError)
    async def _(request: Request, exc: PreferenceCreateError):
        logger.exception("Preference create error: %s", exc)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": str(exc)},
        )

    @app.exception_handler(PreferenceAlreadyExistsError)
    async def _(request: Request, exc: PreferenceAlreadyExistsError):
        logger.exception("Preference already exists error: %s", exc)
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"detail": str(exc)},
        )

    @app.exception_handler(UserNotFoundError)
    async def _(request: Request, exc: UserNotFoundError):
        logger.exception("User not found error: %s", exc)
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": str(exc)},
        )

    @app.exception_handler(UserAlreadyExistsError)
    async def _(request: Request, exc: UserAlreadyExistsError):
        logger.exception("User already exists error: %s", exc)
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"detail": str(exc)},
        )

    @app.exception_handler(UserCreateError)
    async def _(request: Request, exc: UserCreateError):
        logger.exception("User create error: %s", exc)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": str(exc)},
        )

    @app.exception_handler(ConnectionRefusedError)
    async def _(request: Request, exc: ConnectionRefusedError):
        logger.critical("Connection to DB refused: %s", exc)
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"detail": "Connection to DB refused"},
        )

    @app.exception_handler(KafkaConnectionError)
    async def _(request: Request, exc: KafkaConnectionError):
        logger.critical("Connection to Kafka refused: %s", exc)
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"detail": "Connection to Kafka refused"},
        )

    @app.exception_handler(Exception)
    async def _(request: Request, exc: Exception):
        logger.exception("Internal server error: %s", exc)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Internal server error."},
        )

    return app
