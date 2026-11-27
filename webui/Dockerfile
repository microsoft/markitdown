# Build from the repo root:  docker build -f webui/Dockerfile -t markitdown-ui .
FROM python:3.13-slim-trixie

ENV PYTHONUNBUFFERED=1 \
    EXIFTOOL_PATH=/usr/bin/exiftool \
    FFMPEG_PATH=/usr/bin/ffmpeg \
    ORT_DISABLE_TELEMETRY=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends ffmpeg libimage-exiftool-perl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY packages/markitdown /app/packages/markitdown
COPY webui /app/webui
RUN pip --no-cache-dir install "/app/packages/markitdown[all]" -r /app/webui/requirements.txt

RUN useradd -r -u 10001 appuser
USER appuser
WORKDIR /app/webui
EXPOSE 8000
HEALTHCHECK CMD python -c "import urllib.request as u; u.urlopen('http://127.0.0.1:8000/health')"
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
