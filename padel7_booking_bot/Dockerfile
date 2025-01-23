# Use a base image with minimal size and multi-arch support
FROM --platform=$BUILDPLATFORM python:3.12-slim

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV TERM=xterm

# Install basic utilities
RUN apt-get update && apt-get install -y --no-install-recommends \
    gnupg \
    curl \
    wget \
    unzip \
    xvfb \
    libxi6 \
    chromium \
    chromium-l10n \
    libgconf-2-4

# Copy application files
ADD . /app
WORKDIR /app

# Install Chromedriver
# Update ChromeDriver installation step in your Dockerfile to ensure proper architecture
RUN if [ "$(uname -m)" = "aarch64" ]; then \
        unzip driver/chromedriver-v34.0.0-linux-arm64 chromedriver -d /usr/bin/ ;\
    else \
        CHROMEDRIVER_VERSION=$(curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE) \
        && wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/${CHROMEDRIVER_VERSION}/chromedriver_linux64.zip \
        && unzip /tmp/chromedriver.zip chromedriver -d /usr/bin/ \
        && rm /tmp/chromedriver.zip; \
    fi

# Install Python dependencies
RUN pip install -r requirements.txt --no-cache-dir

# Set the entrypoint
ENTRYPOINT ["python", "main.py"]
