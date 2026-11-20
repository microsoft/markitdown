FROM python:3.13-slim-trixie

ENV DEBIAN_FRONTEND=noninteractive
ENV EXIFTOOL_PATH=/usr/bin/exiftool
ENV FFMPEG_PATH=/usr/bin/ffmpeg
ENV MARKITDOWN_ENABLE_PLUGINS=True
ENV ORT_DISABLE_TELEMETRY=1

# Runtime dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ffmpeg \
        libimage-exiftool-perl \
    && rm -rf /var/lib/apt/lists/*

COPY . /app

RUN pip install --no-cache-dir /app

WORKDIR /workdir

ARG USERID=nobody
ARG GROUPID=nogroup

USER ${USERID}:${GROUPID}

ENTRYPOINT ["markitdown-mcp"]
