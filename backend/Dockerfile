FROM python:3.13-slim-bullseye

ENV DEBIAN_FRONTEND=noninteractive
ENV EXIFTOOL_PATH=/usr/bin/exiftool
ENV FFMPEG_PATH=/usr/bin/ffmpeg

RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    exiftool \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install markitdown first
COPY packages /app/packages
RUN pip --no-cache-dir install /app/packages/markitdown[all]

# Install backend dependencies
COPY backend/requirements.txt /app/backend/
RUN pip --no-cache-dir install -r /app/backend/requirements.txt

COPY backend/app.py /app/backend/

EXPOSE 8000

CMD ["python", "/app/backend/app.py"]