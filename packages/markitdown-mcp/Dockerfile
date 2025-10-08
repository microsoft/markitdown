FROM python:3.13-slim-bullseye

ENV DEBIAN_FRONTEND=noninteractive
ENV EXIFTOOL_PATH=/usr/bin/exiftool
ENV FFMPEG_PATH=/usr/bin/ffmpeg
ENV MARKITDOWN_ENABLE_PLUGINS=True

# Runtime dependency
# NOTE: Add any additional MarkItDown plugins here
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    exiftool \
    curl

# Cleanup
RUN rm -rf /var/lib/apt/lists/*

# Copy both packages to ensure we use latest local source for both
COPY packages/markitdown /app/packages/markitdown
COPY packages/markitdown-mcp /app/packages/markitdown-mcp

# Install markitdown from local source first, then markitdown-mcp
# This ensures we use the latest local code for both packages
RUN pip --no-cache-dir install /app/packages/markitdown[all] && \
    pip --no-cache-dir install /app/packages/markitdown-mcp

WORKDIR /workdir

# Default USERID and GROUPID
ARG USERID=nobody
ARG GROUPID=nogroup

USER $USERID:$GROUPID

ENTRYPOINT [ "markitdown-mcp" ]
