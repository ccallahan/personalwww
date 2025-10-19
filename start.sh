#!/bin/bash
# Start script for Reflex app on Railway with Caddy reverse proxy

# Use Railway's PORT or default to 8000
PORT=${PORT:-8000}

# Reflex will run on port 8080 internally (changed from 3000 to avoid conflicts)
REFLEX_PORT=8080

# Set production URLs
export API_URL=https://www.chancecallahan.com
export DEPLOY_URL=https://www.chancecallahan.com

# Start Reflex in the background
reflex run --env prod --loglevel debug --backend-host 127.0.0.1 --backend-port "$REFLEX_PORT" &

# Wait a moment for Reflex to start
sleep 10

# Start Caddy in the foreground (this keeps the container running)
exec caddy run --config /app/Caddyfile --adapter caddyfile
