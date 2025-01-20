FROM python:3.12-slim

# Set environment variables to prevent issues with prompts during installation
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# Install Chrome
RUN apt-get update && apt-get install -y \
    gnupg \
    curl \
    wget \
    unzip \
    xvfb \
    libxi6 \
    libgconf-2-4 \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list' \
    && apt-get update && apt-get install -y \
    google-chrome-stable \
    --no-install-recommends

# Install Chromedriver
RUN CHROMEDRIVER_VERSION=`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE` && \
    wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip && \
    unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/ && \
    rm /tmp/chromedriver.zip


ADD . /app
WORKDIR /app
RUN pip install -r requirements.txt --no-cache-dir
ENTRYPOINT ["python", "main.py"]
