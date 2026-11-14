FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1



COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

COPY bot/pyproject.toml bot/uv.lock ./

RUN uv sync --frozen --no-dev


COPY shared ./shared/
COPY bot ./bot/

ENV PATH="/app/.venv/bin:$PATH"
CMD ["python", "-m", "bot.main"]

