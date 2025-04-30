FROM python:3.10-slim

WORKDIR /app
COPY . .

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    curl \
    ca-certificates \
    fonts-liberation \
    libappindicator3-1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libgbm1 \
    libglib2.0-0 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libpango-1.0-0 \
    libx11-6 \
    libxcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxkbcommon0 \
    libxrandr2 \
    libxshmfence1 \
    libxss1 \
    libxtst6 \
    # Additional dependencies
    libwebpdemux2 \
    libwoff1 \
    libopus0 \
    libwebp7 \          
    libgdk-pixbuf2.0-0 \ 
    libglib-2.0.so.0 \
    libgobject-2.0.so.0 \
    libnss3.so \
    libnssutil3.so \
    libnspr4.so \
    libdbus-1.so.3 \
    libatk-1.0.so.0 \
    libatk-bridge-2.0.so.0 \
    libgio-2.0.so.0 \
    libexpat.so.1 \
    libatspi.so.0 \
    libX11.so.6 \
    libXcomposite.so.1 \
    libXdamage.so.1 \
    libXext.so.6 \
    libXfixes.so.3 \
    libXrandr.so.2\
    libgbm.so.1 \
    libxcb.so.1 \
    libxkbcommon.so.0 \
    libasound.so.2 
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers AFTER pip install
RUN playwright install chromium

CMD ["python", "main.py"]
