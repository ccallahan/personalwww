#!/bin/bash
# Start script for Reflex app on Railway

# Use Railway's PORT or default to 8000
PORT=${PORT:-8000}

# Run Reflex with the expanded port
exec reflex run --env prod --loglevel info --backend-host 0.0.0.0 --backend-port "$PORT"
