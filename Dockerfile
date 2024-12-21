FROM python:3.13-slim-bullseye

USER root

ARG INSTALL_GIT=false
RUN if [ "$INSTALL_GIT" = "true" ]; then \
    apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*; \
    fi

# Runtime dependency
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

RUN pip install markitdown

# Default USERID and GROUPID
ARG USERID=10000
ARG GROUPID=10000

USER $USERID:$GROUPID

ENTRYPOINT [ "markitdown" ]
