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
    chromium-driver \
    chromium-l10n \
    libgconf-2-4

# Copy application files
ADD . /app
WORKDIR /app

# Install Chromedriver
# Update ChromeDriver installation step in your Dockerfile to ensure proper architecture
#RUN if [ "$(uname -m)" = "aarch64" ]; then \
#        unzip driver/chromedriver-v34.0.0-linux-arm64 chromedriver -d /usr/bin/ ;\
#    else \
#        unzip -j driver/chromedriver-linux64.zip chromedriver-linux64/chromedriver -d /usr/bin/ ;\
#    fi

# Install Python dependencies
RUN pip install -r requirements.txt --no-cache-dir

# Set the entrypoint
ENTRYPOINT ["python", "main.py"]
