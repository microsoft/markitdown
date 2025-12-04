FROM python:3.13-slim-bullseye as builder

WORKDIR /build

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy package files
COPY . /build

# Install dependencies
RUN pip install --no-cache-dir \
    /build/packages/markitdown[all] \
    /build/packages/markitdown-api


FROM python:3.13-slim-bullseye

ENV DEBIAN_FRONTEND=noninteractive
ENV EXIFTOOL_PATH=/usr/bin/exiftool
ENV FFMPEG_PATH=/usr/bin/ffmpeg
ENV MARKITDOWN_API_HOST=0.0.0.0
ENV MARKITDOWN_API_PORT=8000
ENV MARKITDOWN_API_WORKERS=2
ENV MARKITDOWN_API_ENABLE_PLUGINS=false
ENV MARKITDOWN_API_RATE_LIMIT=60
ENV MARKITDOWN_API_MAX_FILE_SIZE=10485760

# Runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    exiftool \
    && rm -rf /var/lib/apt/lists/*

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /usr/local/bin/markitdown-api /usr/local/bin/markitdown-api

# Create non-root user
RUN useradd -r -s /bin/false markitdown
USER markitdown

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${MARKITDOWN_API_PORT}/health || exit 1

EXPOSE ${MARKITDOWN_API_PORT}

ENTRYPOINT ["markitdown-api"]