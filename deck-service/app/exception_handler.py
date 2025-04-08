from aiokafka.errors import KafkaConnectionError  # type: ignore
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from domain.exceptions import (
    CandidateNotFoundError,
    DeckCacheClearError,
    DeckCacheError,
    DeckGenerateError,
    DeckNotFoundError,
    PreferenceAlreadyExistsError,
    PreferenceCreateError,
    PreferenceForProfileNotFoundError,
    PreferenceNotFoundError,
    ProfileAlreadyExistsError,
    ProfileCreateError,
    ProfileNotFoundError,
)


def add_exception_handler(app: FastAPI) -> FastAPI:
    @app.exception_handler(CandidateNotFoundError)
    async def _(request: Request, exc: CandidateNotFoundError):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": str(exc)},
        )

    @app.exception_handler(DeckNotFoundError)
    async def _(request: Request, exc: DeckNotFoundError):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": str(exc)},
        )

    @app.exception_handler(DeckGenerateError)
    async def _(request: Request, exc: DeckGenerateError):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": str(exc)},
        )

    @app.exception_handler(DeckCacheError)
    async def _(request: Request, exc: DeckCacheError):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": str(exc)},
        )

    @app.exception_handler(DeckCacheClearError)
    async def _(request: Request, exc: DeckCacheClearError):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": str(exc)},
        )

    @app.exception_handler(PreferenceAlreadyExistsError)
    async def _(request: Request, exc: PreferenceAlreadyExistsError):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"detail": str(exc)},
        )

    @app.exception_handler(PreferenceCreateError)
    async def _(request: Request, exc: PreferenceCreateError):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": str(exc)},
        )

    @app.exception_handler(PreferenceNotFoundError)
    async def _(request: Request, exc: PreferenceNotFoundError):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": str(exc)},
        )

    @app.exception_handler(PreferenceForProfileNotFoundError)
    async def _(request: Request, exc: PreferenceForProfileNotFoundError):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": str(exc)},
        )

    @app.exception_handler(ProfileAlreadyExistsError)
    async def _(request: Request, exc: ProfileAlreadyExistsError):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"detail": str(exc)},
        )

    @app.exception_handler(ProfileCreateError)
    async def _(request: Request, exc: ProfileCreateError):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": str(exc)},
        )

    @app.exception_handler(ProfileNotFoundError)
    async def _(request: Request, exc: ProfileNotFoundError):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": str(exc)},
        )

    @app.exception_handler(ConnectionRefusedError)
    async def _(request: Request, exc: ConnectionRefusedError):
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"detail": "Connection to DB refused"},
        )

    @app.exception_handler(KafkaConnectionError)
    async def _(request: Request, exc: KafkaConnectionError):
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"detail": "Connection to Kafka refused"},
        )

    @app.exception_handler(Exception)
    async def _(request: Request, exc: Exception):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Internal server error."},
        )

    return app
