# 1. Base Image and System Dependencies
FROM python:3.13-slim-bullseye

ENV DEBIAN_FRONTEND=noninteractive
ENV EXIFTOOL_PATH=/usr/bin/exiftool
ENV FFMPEG_PATH=/usr/bin/ffmpeg

# Install runtime dependencies required by markitdown
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    exiftool \
    && rm -rf /var/lib/apt/lists/*

# 2. Set up Application Directory
WORKDIR /app

# 3. Copy application code
COPY . .

# 4. Install Python dependencies
# Installing both markitdown (with all dependencies) and the sample plugin
RUN pip --no-cache-dir install \
    ./packages/markitdown[all] \
    ./packages/markitdown-sample-plugin

# 5. Expose the port the API server will run on
EXPOSE 8000

# 6. Run as a non-root user for better security
RUN useradd -m -u 1000 appuser
USER appuser

# 7. Set the command to run the API server
# Use 0.0.0.0 to make it accessible outside the container
CMD ["uvicorn", "markitdown.api_server:app", "--host", "0.0.0.0", "--port", "8000"]