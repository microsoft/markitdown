# ffmpeg
FROM jrottenberg/ffmpeg:4.1-scratch AS ffmpeg

# Developoment stage
FROM python:3.13-bullseye AS development
# Copy ffmpeg binaries
COPY --from=ffmpeg / /

# Install build dependencies
RUN apt update \
  && apt install -y --no-install-recommends \
  build-essential \
  && apt clean \
  && rm -rf /var/lib/apt/lists/*

# Install Python package
RUN pip install --no-cache-dir markitdown

# Production stage
FROM python:3.13-slim-bullseye AS production
# Copy ffmpeg binaries
COPY --from=ffmpeg / /

# Default USERID and GROUPID
ARG USERID=10000
ARG GROUPID=10000

# Set up user
RUN groupadd -g $GROUPID appgroup && \
    useradd -m -u $USERID -g appgroup appuser

USER $USERID:$GROUPID

# Copy installed dependencies from development stage
COPY --from=development /usr/local /usr/local

# Entrypoint
ENTRYPOINT ["markitdown"]
