# Multi-stage Dockerfile for BrowserClaw
FROM node:20-alpine AS frontend-builder
WORKDIR /app/frontend
COPY src/frontend/package*.json ./
RUN npm install
COPY src/frontend/ ./
RUN npx vite build

FROM python:3.12-slim
WORKDIR /app

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget gnupg curl ca-certificates libglib2.0-0 libnss3 libnspr4 libatk1.0-0 \
    libatk-bridge2.0-0 libcups2 libdrm2 libdbus-1-3 libxcb1 libxkbcommon0 \
    libx11-6 libxcomposite1 libxdamage1 libxext6 libxfixes3 libxrandr2 \
    libgbm1 libpango-1.0-0 libcairo2 libasound2 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt* ./
RUN pip install --no-cache-dir fastapi uvicorn pydantic sqlalchemy aiosqlite playwright httpx pillow pytest \
    && playwright install chromium --with-deps || true

COPY src/ ./src/
COPY --from=frontend-builder /app/frontend/dist ./src/frontend/dist

EXPOSE 8000
CMD ["uvicorn", "src.backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
