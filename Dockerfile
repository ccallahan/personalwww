# Use Python 3.11 slim image
FROM python:3.11-slim

ARG PORT=8080
# Only set for local/direct access. When TLS is used, the API_URL is assumed to be the same as the frontend.
ARG API_URL
ENV PORT=$PORT REFLEX_API_URL=${API_URL:-http://localhost:$PORT} REFLEX_REDIS_URL=redis://localhost PYTHONUNBUFFERED=1

# Install system dependencies including Node.js and Caddy
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    gnupg \
    unzip \
    debian-keyring \
    debian-archive-keyring \
    apt-transport-https \
    redis-server \
    && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg \
    && curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | tee /etc/apt/sources.list.d/caddy-stable.list \
    && apt-get update \
    && apt-get install -y caddy \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy local context to `/app` inside container (see .dockerignore)
COPY . .

# Install app requirements and reflex in the container
RUN pip install -r requirements.txt

# Deploy templates and prepare app
RUN reflex init

# Download all npm dependencies and compile frontend
RUN reflex export --frontend-only --no-zip && mv .web/build/client/* /srv/ && rm -rf .web

# Needed until Reflex properly passes SIGTERM on backend.
STOPSIGNAL SIGKILL

EXPOSE $PORT

# Apply migrations before starting the backend.
CMD [ -d alembic ] && reflex db migrate; \
    caddy start && \
    redis-server --daemonize yes && \
    exec reflex run --env prod --backend-only