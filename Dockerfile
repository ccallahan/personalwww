# Docke# Use Python 3.11 slim image
FROM python:3.11-slim

# Install system dependencies including Node.js and Caddy
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    gnupg \
    unzip \
    debian-keyring \
    debian-archive-keyring \
    apt-transport-https \
    && curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg \
    && curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | tee /etc/apt/sources.list.d/caddy-stable.list \
    && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get update \
    && apt-get install -y nodejs caddy \
    && rm -rf /var/lib/apt/lists/* Reflex app deployment on Railway

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies including Node.js for frontend
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    gnupg \
    unzip \
    && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Make start script executable
RUN chmod +x start.sh

# Initialize Reflex
RUN reflex init

# Expose port (Railway will use $PORT)
EXPOSE 8000

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Run the start script
CMD ["./start.sh"]
