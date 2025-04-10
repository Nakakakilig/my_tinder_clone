from collections.abc import Awaitable, Callable
from contextvars import ContextVar

import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

correlation_id_var = ContextVar("correlation_id", default=None)


def get_correlation_id() -> str:
    cid = correlation_id_var.get()
    return cid if cid else ""


def set_correlation_id(correlation_id: str):
    correlation_id_var.set(correlation_id)  # type: ignore


def generate_correlation_id() -> str:
    return str(uuid.uuid4())


def clear_correlation_id():
    correlation_id_var.set(None)  # type: ignore


class CorrelationIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        correlation_id = request.headers.get("X-Correlation-Id")
        if not correlation_id:
            correlation_id = generate_correlation_id()

        set_correlation_id(correlation_id)

        response: Response = await call_next(request)

        response.headers["X-Correlation-Id"] = correlation_id
        return response
