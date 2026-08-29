FROM --platform=$BUILDPLATFORM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV TERM=xterm
ENV VIRTUAL_ENV=/app/.venv
ENV PATH="/app/.venv/bin:$PATH"
ENV UV_LINK_MODE=copy

RUN apt-get update && apt-get install -y --fix-broken --no-install-recommends \
    gnupg \
    curl \
    wget \
    unzip \
    xvfb \
    libxi6 \
    chromium \
    chromium-driver \
    chromium-l10n

ADD . /app
WORKDIR /app

RUN uv sync --frozen --no-dev

RUN mkdir -p logs screenshots

ENTRYPOINT ["python", "main.py"]
