FROM python:3.10-slim

WORKDIR /app
COPY . .

# Install system dependencies needed for Chromium (Playwright)
RUN apt-get update && apt-get install -y \\
    wget gnupg curl ca-certificates fonts-liberation libappindicator3-1 \\
    libasound2 libatk-bridge2.0-0 libatk1.0-0 libcups2 libdbus-1-3 \\
    libgdk-pixbuf2.0-0 libnspr4 libnss3 libx11-xcb1 libxcomposite1 \\
    libxdamage1 libxrandr2 libgbm1 libxshmfence1 libxss1 libxtst6 \\
    libxext6 libxfixes3 libxrender1 libx11-6 libxkbcommon0 \\
    libglib2.0-0 libgobject-2.0-0 libgtk-3-0 libexpat1 libatspi2.0-0 \\
    --no-install-recommends && rm -rf /var/lib/apt/lists/*

# Install Python dependencies and Playwright
RUN pip install --no-cache-dir -r requirements.txt \\
    && playwright install chromium

CMD ["python", "main.py"]
