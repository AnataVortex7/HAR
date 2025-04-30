FROM python:3.10-slim

ENV PLAYWRIGHT_BROWSERS_PATH=0

WORKDIR /app
COPY . .

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget curl gnupg ca-certificates \
    libglib2.0-0 libnss3 libgdk-pixbuf2.0-0 libgtk-3-0 libxss1 \
    libasound2 libxshmfence1 libxrandr2 libatk1.0-0 libatk-bridge2.0-0 \
    libx11-xcb1 libxcomposite1 libxdamage1 libxext6 libxfixes3 libgbm1 \
    libpango-1.0-0 libcups2 libxkbcommon0 libx11-6 libxcb1 libnspr4 \
    fonts-liberation --no-install-recommends && rm -rf /var/lib/apt/lists/*

# Install Python & Playwright and its browser
RUN pip install --no-cache-dir -r requirements.txt \
 && playwright install chromium

CMD ["python", "main.py"]
