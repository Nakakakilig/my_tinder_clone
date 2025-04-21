FROM python:3.12.3-slim

ENV PYTHONBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# install uv
COPY --from=ghcr.io/astral-sh/uv:0.6.14 /uv /uvx /bin/

WORKDIR /app
COPY pyproject.toml .
COPY uv.lock .

RUN uv sync --frozen --no-cache

COPY profile-service .

RUN chmod +x app/prestart.sh

ENTRYPOINT [ "app/prestart.sh" ]

CMD ["uv", "run", "main.py", "--host", "0.0.0.0", "--port", "8000"]
