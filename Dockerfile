FROM python:3.13-slim-bullseye

ARG INSTALL_GIT=false
RUN if [ "$INSTALL_GIT" = "true" ]; then \
    apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*; \
    fi

# Runtime dependency
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . /app
RUN pip --no-cache-dir install .

# Default USERID and GROUPID
ARG USERID=nobody
ARG GROUPID=nogroup

USER $USERID:$GROUPID

ENTRYPOINT [ "markitdown" ]
