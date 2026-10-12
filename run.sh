#!/usr/bin/env bash
set -e
echo "🦈 Launching BrowserClaw..."
export PYTHONPATH="src:.":$PYTHONPATH

# Ensure frontend build exists
if [ ! -d "src/frontend/dist" ]; then
    echo "📦 Building frontend..."
    cd src/frontend && npm install && npx vite build && cd ../..
fi

echo "🚀 Starting BrowserClaw API on http://0.0.0.0:8000"
exec python3 -m uvicorn src.backend.app.main:app --host 0.0.0.0 --port 8000 --reload
