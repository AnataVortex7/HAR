FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y wget gnupg curl && \
    pip install --no-cache-dir -r requirements.txt && \
    playwright install chromium

CMD ["python", "main.py"]
