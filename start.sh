#!/bin/bash
# Start script for Reflex app on Railway

# Use Railway's PORT or default to 8000
PORT=${PORT:-8000}

# Set production URLs - these MUST be set before running
export API_URL=${API_URL:-https://www.chancecallahan.com}
export DEPLOY_URL=${DEPLOY_URL:-https://www.chancecallahan.com}

# Run Reflex in production mode
exec reflex run --env prod --loglevel debug --backend-host 0.0.0.0 --backend-port "$PORT"
