FROM python:3.13-slim-bullseye

ENV DEBIAN_FRONTEND=noninteractive
ENV EXIFTOOL_PATH=/usr/local/bin/exiftool
ENV FFMPEG_PATH=/usr/bin/ffmpeg
ENV MARKITDOWN_ENABLE_PLUGINS=True

# Runtime dependency
# NOTE: Add any additional MarkItDown plugins here
# Install build tools temporarily for ExifTool compilation
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    curl \
    wget \
    perl \
    make && \
    rm -rf /var/lib/apt/lists/*

# Install ExifTool from source (latest version to avoid CVE-2021-22204)
# The Debian package (libimage-exiftool-perl) is too old (12.16), we need 12.24+
RUN wget https://exiftool.org/Image-ExifTool-13.38.tar.gz && \
    tar -xzf Image-ExifTool-13.38.tar.gz && \
    cd Image-ExifTool-13.38 && \
    perl Makefile.PL && \
    make && \
    make install && \
    cd .. && \
    rm -rf Image-ExifTool-13.38 Image-ExifTool-13.38.tar.gz

# Cache-busting: Add build arg to force rebuild when code changes
ARG CACHE_BUST=unknown
RUN echo "Cache bust: $CACHE_BUST"

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
