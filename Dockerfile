# Dockerfile for Reflex app deployment on Railway

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

# Initialize Reflex and export for production
RUN reflex init
RUN reflex export --frontend-only --no-zip

# Expose port (Railway will use $PORT)
EXPOSE 8000

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Run the Reflex app in production mode
CMD reflex run --env prod --loglevel info --backend-host 0.0.0.0 --backend-port $PORT
