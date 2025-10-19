#!/bin/bash
# Start script for Reflex app on Railway

# Use Railway's PORT or default to 8000
PORT=${PORT:-8000}

# Set the API URL environment variable for production
export API_URL="https://www.chancecallahan.com"

# Run Reflex in production mode
# In prod mode, backend serves both API and the exported frontend
exec reflex run --env prod --loglevel info --backend-host 0.0.0.0 --backend-port "$PORT"
