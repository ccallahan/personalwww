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
