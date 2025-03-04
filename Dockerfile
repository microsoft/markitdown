# FFmpeg stage
FROM jrottenberg/ffmpeg:4.1-scratch AS ffmpeg

# Development stage
FROM python:3.13-bullseye AS development

COPY --from=ffmpeg / /

ENV PYTHONUNBUFFERED=1 \
  PYTHONDONTWRITEBYTECODE=1

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
  build-essential \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir hatch

WORKDIR /app
COPY . /app/

# Build stage
FROM python:3.13-bullseye AS build

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
  build-essential \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir hatch

WORKDIR /app

COPY pyproject.toml /app/
COPY . /app/

RUN hatch build

# Production stage
FROM python:3.13-slim-bullseye AS production

# Copy ffmpeg binaries
COPY --from=ffmpeg / /

WORKDIR /app

COPY --from=build /app/dist /tmp/dist

RUN pip install --no-cache-dir /tmp/dist/markitdown-*.whl

# Default USERID and GROUPID
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# Entrypoint
ENTRYPOINT ["markitdown"]
